from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Case, When, IntegerField, Value
from .models import Protein, Interaction
from .serializers import ProteinSerializer, InteractionSerializer


class ProteinViewSet(viewsets.ModelViewSet):
    """
    API endpoint for proteins.
    Supports searching by gene_name, protein_name, uniprot_id, or description.
    Results are ranked: exact gene name match first, then starts-with, then others.
    """
    queryset = Protein.objects.none()
    serializer_class = ProteinSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['gene_name', 'protein_name', 'uniprot_id', 'description']

    def get_queryset(self):
        queryset = Protein.objects.all()
        search = self.request.query_params.get('search', '').strip()
        if search:
            queryset = queryset.annotate(
                relevance=Case(
                    When(gene_name__iexact=search, then=Value(0)),
                    When(gene_name__istartswith=search, then=Value(1)),
                    When(uniprot_id__iexact=search, then=Value(2)),
                    default=Value(3),
                    output_field=IntegerField(),
                )
            ).order_by('relevance', 'gene_name')
        else:
            queryset = queryset.order_by('gene_name')
        return queryset


class InteractionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for protein-protein interactions.
    Filter by gene name: GET /api/interactions/?protein=TP53
    """
    serializer_class = InteractionSerializer

    def get_queryset(self):
        queryset = Interaction.objects.select_related('protein_a', 'protein_b').all()
        protein = self.request.query_params.get('protein', None)
        if protein:
            queryset = queryset.filter(
                Q(protein_a__gene_name__icontains=protein) |
                Q(protein_b__gene_name__icontains=protein)
            )
        return queryset


class UploadView(APIView):
    """
    POST /api/upload/ — Upload a TSV/CSV file of protein interactions.
    TSV/TXT: col0=UniProt_A, col1=UniProt_B (PSI-MI TAB format)
    CSV: columns gene_a, gene_b, score, dataset
    """
    def post(self, request):
        try:
            import pandas as pd
            import io
        except ImportError:
            return Response({'error': 'pandas not installed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        filename = file.name.lower()
        content = file.read().decode('utf-8')

        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(content))
                required = {'gene_a', 'gene_b', 'score', 'dataset'}
                if not required.issubset(df.columns):
                    return Response(
                        {'error': f'CSV must have columns: {required}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            elif filename.endswith(('.tsv', '.txt')):
                df = pd.read_csv(io.StringIO(content), sep='\t', header=None)
                df.columns = ['uniprot_a', 'uniprot_b'] + list(df.columns[2:])
                df['gene_a'] = df['uniprot_a']
                df['gene_b'] = df['uniprot_b']
                df['score'] = 0.5
                df['dataset'] = 'uploaded'
            else:
                return Response({'error': 'File must be .csv, .tsv, or .txt'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Failed to parse file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        success_rows = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                protein_a = Protein.objects.filter(
                    Q(gene_name__iexact=str(row['gene_a'])) |
                    Q(uniprot_id__iexact=str(row.get('uniprot_a', row['gene_a'])))
                ).first()
                protein_b = Protein.objects.filter(
                    Q(gene_name__iexact=str(row['gene_b'])) |
                    Q(uniprot_id__iexact=str(row.get('uniprot_b', row['gene_b'])))
                ).first()

                if not protein_a:
                    errors.append({'row': int(idx) + 1, 'message': f'Protein not found: {row["gene_a"]}'})
                    continue
                if not protein_b:
                    errors.append({'row': int(idx) + 1, 'message': f'Protein not found: {row["gene_b"]}'})
                    continue

                Interaction.objects.get_or_create(
                    protein_a=protein_a,
                    protein_b=protein_b,
                    dataset=str(row.get('dataset', 'uploaded')),
                    defaults={
                        'score': float(row.get('score', 0.5)),
                        'interaction_type': 'physical',
                    }
                )
                success_rows += 1
            except Exception as e:
                errors.append({'row': int(idx) + 1, 'message': str(e)})

        return Response({'success_rows': success_rows, 'errors': errors})
