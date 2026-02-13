from rest_framework import serializers
from .models import Protein

class ProteinSerializer(serializers.ModelSerializer):
    """
    Serializer for Protein model - converts to/from JSON.
    """
    class Meta:
        model = Protein
        fields = [
            'id',
            'gene_name',
            'protein_name',
            'uniprot_id',
            'ensembl_id',
            'entrez_id',
            'description',
            'sequence',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
