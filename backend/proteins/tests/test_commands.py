"""
Tests for the load_sample_proteins management command.
"""
from django.test import TestCase
from django.core.management import call_command
from io import StringIO
from proteins.models import Protein, Interaction


class LoadSampleProteinsCommandTest(TestCase):
    """Tests for the load_sample_proteins management command."""

    def test_command_creates_proteins(self):
        """Running the command should create sample proteins."""
        self.assertEqual(Protein.objects.count(), 0)
        out = StringIO()
        call_command('load_sample_proteins', stdout=out)
        self.assertGreater(Protein.objects.count(), 0)
        # The command creates 7 proteins based on the source
        self.assertEqual(Protein.objects.count(), 7)

    def test_command_creates_interactions(self):
        """Running the command should create sample interactions."""
        self.assertEqual(Interaction.objects.count(), 0)
        out = StringIO()
        call_command('load_sample_proteins', stdout=out)
        self.assertGreater(Interaction.objects.count(), 0)
        # The command creates 10 interactions based on the source
        self.assertEqual(Interaction.objects.count(), 10)

    def test_command_is_idempotent(self):
        """Running the command twice should not create duplicate records."""
        out = StringIO()
        call_command('load_sample_proteins', stdout=out)
        protein_count = Protein.objects.count()
        interaction_count = Interaction.objects.count()

        # Run a second time
        call_command('load_sample_proteins', stdout=out)
        self.assertEqual(Protein.objects.count(), protein_count)
        self.assertEqual(Interaction.objects.count(), interaction_count)

    def test_command_output_contains_success_messages(self):
        """Command output should contain success messages."""
        out = StringIO()
        call_command('load_sample_proteins', stdout=out)
        output = out.getvalue()
        self.assertIn('Loading sample proteins', output)
        self.assertIn('Total proteins', output)
        self.assertIn('Loading sample interactions', output)
        self.assertIn('Total interactions', output)
