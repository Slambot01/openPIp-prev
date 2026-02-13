from rest_framework import viewsets, filters
from .models import Protein
from .serializers import ProteinSerializer

class ProteinViewSet(viewsets.ModelViewSet):
    """
    API endpoint for proteins.
    Provides list, create, retrieve, update, and destroy actions.
    Supports searching by gene_name, protein_name, uniprot_id, or description.
    """
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['gene_name', 'protein_name', 'uniprot_id', 'description']
    ordering_fields = ['gene_name', 'created_at']
    ordering = ['gene_name']
