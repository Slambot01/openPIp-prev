from rest_framework import serializers
from .models import Protein, Interaction

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


class InteractionSerializer(serializers.ModelSerializer):
    """
    Serializer for Interaction model with nested protein data.
    """
    protein_a = ProteinSerializer(read_only=True)
    protein_b = ProteinSerializer(read_only=True)

    class Meta:
        model = Interaction
        fields = [
            'id',
            'protein_a',
            'protein_b',
            'score',
            'interaction_type',
            'dataset',
            'created_at',
        ]
        read_only_fields = ['created_at']
