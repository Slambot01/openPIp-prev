from django.db import models

class Protein(models.Model):
    """
    Model representing a protein with basic information.
    Based on the original openPIP protein structure.
    """
    gene_name = models.CharField(max_length=100, help_text="Gene symbol (e.g., TP53)")
    protein_name = models.CharField(max_length=200, blank=True, help_text="Full protein name")
    uniprot_id = models.CharField(max_length=50, unique=True, help_text="UniProt accession ID")
    ensembl_id = models.CharField(max_length=100, blank=True, help_text="Ensembl gene ID")
    entrez_id = models.CharField(max_length=100, blank=True, help_text="Entrez/NCBI gene ID")
    description = models.TextField(blank=True, help_text="Protein function description")
    sequence = models.TextField(blank=True, help_text="Amino acid sequence")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['gene_name']
        verbose_name = 'Protein'
        verbose_name_plural = 'Proteins'

    def __str__(self):
        return f"{self.gene_name} ({self.uniprot_id})"
