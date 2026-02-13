"""
Script to load sample protein data into the database.
Run with: python manage.py shell < load_sample_data.py
"""

from proteins.models import Protein

# Sample proteins from well-known human genes
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
        'description': 'DNA repair protein that plays a role in maintaining genomic stability',
    },
    {
        'gene_name': 'EGFR',
        'protein_name': 'Epidermal growth factor receptor',
        'uniprot_id': 'P00533',
        'ensembl_id': 'ENSG00000146648',
        'entrez_id': '1956',
        'description': 'Receptor tyrosine kinase that binds to epidermal growth factor',
    },
    {
        'gene_name': 'MYC',
        'protein_name': 'Myc proto-oncogene protein',
        'uniprot_id': 'P01106',
        'ensembl_id': 'ENSG00000136997',
        'entrez_id': '4609',
        'description': 'Transcription factor that is a global regulator of gene expression',
    },
    {
        'gene_name': 'KRAS',
        'protein_name': 'GTPase KRas',
        'uniprot_id': 'P01116',
        'ensembl_id': 'ENSG00000133703',
        'entrez_id': '3845',
        'description': 'GTPase involved in signal transduction pathways',
    },
    {
        'gene_name': 'PTEN',
        'protein_name': 'Phosphatidylinositol 3,4,5-trisphosphate 3-phosphatase',
        'uniprot_id': 'P60484',
        'ensembl_id': 'ENSG00000171862',
        'entrez_id': '5728',
        'description': 'Tumor suppressor that regulates cell cycle and cell survival',
    },
    {
        'gene_name': 'RB1',
        'protein_name': 'Retinoblastoma-associated protein',
        'uniprot_id': 'P06400',
        'ensembl_id': 'ENSG00000139687',
        'entrez_id': '5925',
        'description': 'Key regulator of entry into cell division',
    },
    {
        'gene_name': 'AKT1',
        'protein_name': 'RAC-alpha serine/threonine-protein kinase',
        'uniprot_id': 'P31749',
        'ensembl_id': 'ENSG00000142208',
        'entrez_id': '207',
        'description': 'Serine/threonine kinase that regulates cell survival',
    },
]

print("Loading sample proteins...")
for protein_data in sample_proteins:
    protein, created = Protein.objects.get_or_create(
        uniprot_id=protein_data['uniprot_id'],
        defaults=protein_data
    )
    if created:
        print(f"✓ Created: {protein.gene_name} ({protein.uniprot_id})")
    else:
        print(f"→ Already exists: {protein.gene_name}")

print(f"\nTotal proteins in database: {Protein.objects.count()}")
