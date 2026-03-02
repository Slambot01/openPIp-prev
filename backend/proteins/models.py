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


class Interaction(models.Model):
    """
    Model representing a protein-protein interaction (PPI).
    """
    INTERACTION_TYPES = [
        ('physical', 'Physical'),
        ('genetic', 'Genetic'),
        ('regulatory', 'Regulatory'),
        ('predicted', 'Predicted'),
    ]

    protein_a = models.ForeignKey(Protein, on_delete=models.CASCADE, related_name='interactions_as_a')
    protein_b = models.ForeignKey(Protein, on_delete=models.CASCADE, related_name='interactions_as_b')
    score = models.FloatField(help_text="Interaction confidence score (0-1)")
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_TYPES, default='physical')
    dataset = models.CharField(max_length=200, help_text="Source dataset (e.g., STRING, BioGRID)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']
        verbose_name = 'Interaction'
        verbose_name_plural = 'Interactions'
        unique_together = [['protein_a', 'protein_b', 'dataset']]

    def __str__(self):
        return f"{self.protein_a.gene_name} ↔ {self.protein_b.gene_name} ({self.score:.2f})"

