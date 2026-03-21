"""
Tests for Django admin registration and changelist pages.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.admin.sites import site as admin_site
from proteins.models import Protein, Interaction


class AdminRegistrationTest(TestCase):
    """Tests that models are registered with the admin site."""

    def test_protein_registered(self):
        """Protein model should be registered in admin."""
        self.assertIn(Protein, admin_site._registry)

    def test_interaction_registered(self):
        """Interaction model should be registered in admin."""
        self.assertIn(Interaction, admin_site._registry)


class AdminChangelistTest(TestCase):
    """Tests that admin changelist pages load successfully."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', password='testpass123', email='admin@test.com',
        )
        self.client = Client()
        self.client.login(username='admin', password='testpass123')
        # Create sample data for the changelist
        self.protein = Protein.objects.create(
            gene_name='TP53', uniprot_id='P04637',
        )

    def test_protein_changelist_loads(self):
        """Protein admin changelist should return 200."""
        response = self.client.get('/admin/proteins/protein/')
        self.assertEqual(response.status_code, 200)

    def test_interaction_changelist_loads(self):
        """Interaction admin changelist should return 200."""
        response = self.client.get('/admin/proteins/interaction/')
        self.assertEqual(response.status_code, 200)
