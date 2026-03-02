from django.core.management.base import BaseCommand
from proteins.models import Protein, Interaction

class Command(BaseCommand):
    help = 'Load sample protein data and interactions into the database'

    def handle(self, *args, **kwargs):
        sample_proteins = [
            {
                'gene_name': 'TP53',
                'protein_name': 'Cellular tumor antigen p53',
                'uniprot_id': 'P04637',
                'ensembl_id': 'ENSG00000141510',
                'entrez_id': '7157',
                'description': 'Acts as a tumor suppressor in many tumor types; induces growth arrest or apoptosis',
            },
            {
                'gene_name': 'BRCA1',
                'protein_name': 'Breast cancer type 1 susceptibility protein',
                'uniprot_id': 'P38398',
                'ensembl_id': 'ENSG00000012048',
                'entrez_id': '672',
                'description': 'DNA repair protein involved in double-strand break repair',
            },
            {
                'gene_name': 'EGFR',
                'protein_name': 'Epidermal growth factor receptor',
                'uniprot_id': 'P00533',
                'ensembl_id': 'ENSG00000146648',
                'entrez_id': '1956',
                'description': 'Receptor tyrosine kinase involved in cell growth and differentiation',
            },
            {
                'gene_name': 'MYC',
                'protein_name': 'Myc proto-oncogene protein',
                'uniprot_id': 'P01106',
                'ensembl_id': 'ENSG00000136997',
                'entrez_id': '4609',
                'description': 'Transcription factor that regulates cell cycle progression',
            },
            {
                'gene_name': 'KRAS',
                'protein_name': 'GTPase KRas',
                'uniprot_id': 'P01116',
                'ensembl_id': 'ENSG00000133703',
                'entrez_id': '3845',
                'description': 'GTPase involved in signal transduction; frequently mutated in cancer',
            },
            {
                'gene_name': 'MDM2',
                'protein_name': 'E3 ubiquitin-protein ligase Mdm2',
                'uniprot_id': 'Q00987',
                'ensembl_id': 'ENSG00000135679',
                'entrez_id': '4193',
                'description': 'Negative regulator of TP53; promotes TP53 degradation via ubiquitination',
            },
            {
                'gene_name': 'BARD1',
                'protein_name': 'BRCA1-associated RING domain protein 1',
                'uniprot_id': 'Q99728',
                'ensembl_id': 'ENSG00000138376',
                'entrez_id': '580',
                'description': 'Forms a heterodimer with BRCA1; involved in DNA damage response',
            },
        ]

        self.stdout.write('Loading sample proteins...')
        protein_objects = {}
        for protein_data in sample_proteins:
            protein, created = Protein.objects.get_or_create(
                uniprot_id=protein_data['uniprot_id'],
                defaults=protein_data
            )
            protein_objects[protein_data['gene_name']] = protein
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {protein.gene_name}'))
            else:
                self.stdout.write(f'  → Already exists: {protein.gene_name}')

        total = Protein.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal proteins: {total}'))

        # Seed interactions
        interactions = [
            ('TP53', 'MDM2', 0.99, 'physical', 'STRING'),
            ('TP53', 'BRCA1', 0.87, 'physical', 'BioGRID'),
            ('BRCA1', 'BARD1', 0.98, 'physical', 'STRING'),
            ('EGFR', 'MYC', 0.72, 'regulatory', 'STRING'),
            ('MYC', 'KRAS', 0.65, 'genetic', 'BioGRID'),
            ('TP53', 'EGFR', 0.75, 'regulatory', 'STRING'),
            ('KRAS', 'EGFR', 0.88, 'physical', 'BioGRID'),
            ('MYC', 'BRCA1', 0.60, 'genetic', 'STRING'),
            ('MDM2', 'KRAS', 0.55, 'predicted', 'STRING'),
            ('BARD1', 'TP53', 0.70, 'physical', 'BioGRID'),
        ]

        self.stdout.write('\nLoading sample interactions...')
        for gene_a, gene_b, score, itype, dataset in interactions:
            pa = protein_objects.get(gene_a)
            pb = protein_objects.get(gene_b)
            if pa and pb:
                interaction, created = Interaction.objects.get_or_create(
                    protein_a=pa,
                    protein_b=pb,
                    dataset=dataset,
                    defaults={'score': score, 'interaction_type': itype}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ {gene_a} ↔ {gene_b} ({score})'))
                else:
                    self.stdout.write(f'  → Already exists: {gene_a} ↔ {gene_b}')

        total_i = Interaction.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal interactions: {total_i}'))
