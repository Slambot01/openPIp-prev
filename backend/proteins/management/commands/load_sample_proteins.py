from django.core.management.base import BaseCommand
from proteins.models import Protein

class Command(BaseCommand):
    help = 'Load sample protein data into the database'

    def handle(self, *args, **kwargs):
        sample_proteins = [
            {
                'gene_name': 'TP53',
                'protein_name': 'Cellular tumor antigen p53',
                'uniprot_id': 'P04637',
                'ensembl_id': 'ENSG00000141510',
                'entrez_id': '7157',
                'description': 'Acts as a tumor suppressor in many tumor types',
            },
            {
                'gene_name': 'BRCA1',
                'protein_name': 'Breast cancer type 1 susceptibility protein',
                'uniprot_id': 'P38398',
                'ensembl_id': 'ENSG00000012048',
                'entrez_id': '672',
                'description': 'DNA repair protein',
            },
            {
                'gene_name': 'EGFR',
                'protein_name': 'Epidermal growth factor receptor',
                'uniprot_id': 'P00533',
                'ensembl_id': 'ENSG00000146648',
                'entrez_id': '1956',
                'description': 'Receptor tyrosine kinase',
            },
            {
                'gene_name': 'MYC',
                'protein_name': 'Myc proto-oncogene protein',
                'uniprot_id': 'P01106',
                'ensembl_id': 'ENSG00000136997',
                'entrez_id': '4609',
                'description': 'Transcription factor',
            },
            {
                'gene_name': 'KRAS',
                'protein_name': 'GTPase KRas',
                'uniprot_id': 'P01116',
                'ensembl_id': 'ENSG00000133703',
                'entrez_id': '3845',
                'description': 'GTPase in signal transduction',
            },
        ]

        self.stdout.write("Loading sample proteins...")
        for protein_data in sample_proteins:
            protein, created = Protein.objects.get_or_create(
                uniprot_id=protein_data['uniprot_id'],
                defaults=protein_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {protein.gene_name}'))
            else:
                self.stdout.write(f'→ Already exists: {protein.gene_name}')

        total = Protein.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal proteins: {total}'))
