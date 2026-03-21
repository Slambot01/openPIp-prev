"""
Tests for the Protein and Interaction models.
"""
from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone
from proteins.models import Protein, Interaction


class ProteinModelTest(TestCase):
    """Tests for the Protein model."""

    def setUp(self):
        self.protein = Protein.objects.create(
            gene_name='TP53',
            protein_name='Cellular tumor antigen p53',
            uniprot_id='P04637',
            ensembl_id='ENSG00000141510',
            entrez_id='7157',
            description='Acts as a tumor suppressor',
            sequence='MEEPQSDPSVEPPLSQETFSDLWK',
        )

    def test_create_protein_with_all_fields(self):
        """A protein created with all fields should persist them correctly."""
        self.assertEqual(self.protein.gene_name, 'TP53')
        self.assertEqual(self.protein.protein_name, 'Cellular tumor antigen p53')
        self.assertEqual(self.protein.uniprot_id, 'P04637')
        self.assertEqual(self.protein.ensembl_id, 'ENSG00000141510')
        self.assertEqual(self.protein.entrez_id, '7157')
        self.assertEqual(self.protein.description, 'Acts as a tumor suppressor')
        self.assertEqual(self.protein.sequence, 'MEEPQSDPSVEPPLSQETFSDLWK')

    def test_str_representation(self):
        """__str__ should return 'GENE (UNIPROT_ID)' format."""
        self.assertEqual(str(self.protein), 'TP53 (P04637)')

    def test_uniprot_id_unique_constraint(self):
        """Duplicate uniprot_id should raise IntegrityError."""
        with self.assertRaises(IntegrityError):
            Protein.objects.create(
                gene_name='DUPLICATE',
                uniprot_id='P04637',  # same as setUp protein
            )

    def test_default_ordering_by_gene_name(self):
        """Proteins should be ordered by gene_name ascending."""
        Protein.objects.create(gene_name='BRCA1', uniprot_id='P38398')
        Protein.objects.create(gene_name='AKT1', uniprot_id='P31749')
        names = list(Protein.objects.values_list('gene_name', flat=True))
        self.assertEqual(names, sorted(names))

    def test_created_at_auto_set(self):
        """created_at should be automatically populated."""
        self.assertIsNotNone(self.protein.created_at)
        self.assertAlmostEqual(
            self.protein.created_at, timezone.now(),
            delta=timezone.timedelta(seconds=5),
        )

    def test_updated_at_auto_set(self):
        """updated_at should be automatically populated and change on save."""
        old_updated = self.protein.updated_at
        self.protein.gene_name = 'TP53_UPDATED'
        self.protein.save()
        self.protein.refresh_from_db()
        self.assertGreaterEqual(self.protein.updated_at, old_updated)

    def test_blank_optional_fields(self):
        """Optional fields should accept empty strings."""
        protein = Protein.objects.create(
            gene_name='MINIMAL',
            uniprot_id='XMINIMAL',
            protein_name='',
            ensembl_id='',
            entrez_id='',
            description='',
            sequence='',
        )
        self.assertEqual(protein.protein_name, '')
        self.assertEqual(protein.ensembl_id, '')
        self.assertEqual(protein.entrez_id, '')
        self.assertEqual(protein.description, '')
        self.assertEqual(protein.sequence, '')

    def test_verbose_names(self):
        """Meta verbose names should be set correctly."""
        self.assertEqual(Protein._meta.verbose_name, 'Protein')
        self.assertEqual(Protein._meta.verbose_name_plural, 'Proteins')


class InteractionModelTest(TestCase):
    """Tests for the Interaction model."""

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
            score=0.95,
            interaction_type='physical',
            dataset='STRING',
        )

    def test_create_interaction_with_all_fields(self):
        """An interaction should persist all fields correctly."""
        self.assertEqual(self.interaction.protein_a, self.protein_a)
        self.assertEqual(self.interaction.protein_b, self.protein_b)
        self.assertAlmostEqual(self.interaction.score, 0.95)
        self.assertEqual(self.interaction.interaction_type, 'physical')
        self.assertEqual(self.interaction.dataset, 'STRING')

    def test_str_representation(self):
        """__str__ should return 'A ↔ B (score)' format."""
        expected = 'TP53 ↔ MDM2 (0.95)'
        self.assertEqual(str(self.interaction), expected)

    def test_unique_together_constraint(self):
        """Duplicate (protein_a, protein_b, dataset) should raise IntegrityError."""
        with self.assertRaises(IntegrityError):
            Interaction.objects.create(
                protein_a=self.protein_a,
                protein_b=self.protein_b,
                score=0.50,
                dataset='STRING',  # same combination
            )

    def test_same_proteins_different_dataset_allowed(self):
        """Same protein pair with different dataset should be allowed."""
        interaction2 = Interaction.objects.create(
            protein_a=self.protein_a,
            protein_b=self.protein_b,
            score=0.80,
            dataset='BioGRID',  # different dataset
        )
        self.assertEqual(Interaction.objects.count(), 2)

    def test_default_ordering_by_score_descending(self):
        """Interactions should be ordered by score descending."""
        Interaction.objects.create(
            protein_a=self.protein_b,
            protein_b=self.protein_a,
            score=0.50,
            dataset='BioGRID',
        )
        scores = list(Interaction.objects.values_list('score', flat=True))
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_cascade_delete_protein_a(self):
        """Deleting protein_a should cascade delete its interactions."""
        self.protein_a.delete()
        self.assertEqual(Interaction.objects.count(), 0)

    def test_cascade_delete_protein_b(self):
        """Deleting protein_b should cascade delete its interactions."""
        self.protein_b.delete()
        self.assertEqual(Interaction.objects.count(), 0)

    def test_default_interaction_type(self):
        """Default interaction_type should be 'physical'."""
        interaction = Interaction.objects.create(
            protein_a=self.protein_b,
            protein_b=self.protein_a,
            score=0.70,
            dataset='TestDB',
        )
        self.assertEqual(interaction.interaction_type, 'physical')

    def test_verbose_names(self):
        """Meta verbose names should be set correctly."""
        self.assertEqual(Interaction._meta.verbose_name, 'Interaction')
        self.assertEqual(Interaction._meta.verbose_name_plural, 'Interactions')

    def test_created_at_auto_set(self):
        """created_at should be automatically populated."""
        self.assertIsNotNone(self.interaction.created_at)
