"""
Tests for ProteinSerializer and InteractionSerializer.
"""
from django.test import TestCase
from proteins.models import Protein, Interaction
from proteins.serializers import ProteinSerializer, InteractionSerializer


class ProteinSerializerTest(TestCase):
    """Tests for ProteinSerializer."""

    def setUp(self):
        self.protein = Protein.objects.create(
            gene_name='TP53',
            protein_name='Cellular tumor antigen p53',
            uniprot_id='P04637',
            ensembl_id='ENSG00000141510',
            entrez_id='7157',
            description='Tumor suppressor',
            sequence='MEEPQSDP',
        )
        self.serializer = ProteinSerializer(instance=self.protein)

    def test_contains_expected_fields(self):
        """Serialized data should contain all expected fields."""
        expected_fields = {
            'id', 'gene_name', 'protein_name', 'uniprot_id',
            'ensembl_id', 'entrez_id', 'description', 'sequence',
            'created_at', 'updated_at',
        }
        self.assertEqual(set(self.serializer.data.keys()), expected_fields)

    def test_field_values_match(self):
        """Serialized field values should match the model instance."""
        data = self.serializer.data
        self.assertEqual(data['gene_name'], 'TP53')
        self.assertEqual(data['uniprot_id'], 'P04637')
        self.assertEqual(data['protein_name'], 'Cellular tumor antigen p53')

    def test_read_only_fields(self):
        """created_at and updated_at should be read-only."""
        read_only = ProteinSerializer.Meta.read_only_fields
        self.assertIn('created_at', read_only)
        self.assertIn('updated_at', read_only)

    def test_valid_deserialization(self):
        """Valid data should deserialize successfully."""
        data = {
            'gene_name': 'BRCA1',
            'protein_name': 'Breast cancer type 1',
            'uniprot_id': 'P38398',
            'ensembl_id': 'ENSG00000012048',
            'entrez_id': '672',
            'description': 'DNA repair',
            'sequence': 'MDLSALREVE',
        }
        serializer = ProteinSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_required_field_gene_name(self):
        """Missing gene_name should fail validation."""
        data = {'uniprot_id': 'XTEST'}
        serializer = ProteinSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('gene_name', serializer.errors)

    def test_missing_required_field_uniprot_id(self):
        """Missing uniprot_id should fail validation."""
        data = {'gene_name': 'TEST'}
        serializer = ProteinSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('uniprot_id', serializer.errors)

    def test_duplicate_uniprot_id_fails_validation(self):
        """Duplicate uniprot_id should fail serializer validation."""
        data = {
            'gene_name': 'DUP',
            'uniprot_id': 'P04637',  # already exists
        }
        serializer = ProteinSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('uniprot_id', serializer.errors)


class InteractionSerializerTest(TestCase):
    """Tests for InteractionSerializer."""

    def setUp(self):
        self.protein_a = Protein.objects.create(
            gene_name='TP53', uniprot_id='P04637',
        )
        self.protein_b = Protein.objects.create(
            gene_name='MDM2', uniprot_id='Q00987',
        )
        self.interaction = Interaction.objects.create(
            protein_a=self.protein_a,
            protein_b=self.protein_b,
            score=0.99,
            interaction_type='physical',
            dataset='STRING',
        )
        self.serializer = InteractionSerializer(instance=self.interaction)

    def test_contains_expected_fields(self):
        """Serialized data should contain all expected fields."""
        expected_fields = {
            'id', 'protein_a', 'protein_b', 'score',
            'interaction_type', 'dataset', 'created_at',
        }
        self.assertEqual(set(self.serializer.data.keys()), expected_fields)

    def test_nested_protein_data(self):
        """protein_a and protein_b should be nested serialized objects."""
        data = self.serializer.data
        # protein_a should be a dict (nested), not just an ID
        self.assertIsInstance(data['protein_a'], dict)
        self.assertIsInstance(data['protein_b'], dict)
        self.assertEqual(data['protein_a']['gene_name'], 'TP53')
        self.assertEqual(data['protein_b']['gene_name'], 'MDM2')

    def test_read_only_created_at(self):
        """created_at should be read-only."""
        read_only = InteractionSerializer.Meta.read_only_fields
        self.assertIn('created_at', read_only)
