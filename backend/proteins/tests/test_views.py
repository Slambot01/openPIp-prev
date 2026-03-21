"""
Tests for ProteinViewSet, InteractionViewSet, and UploadView.
"""
import io
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from proteins.models import Protein, Interaction


class ProteinViewSetTest(TestCase):
    """Tests for the ProteinViewSet API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.protein = Protein.objects.create(
            gene_name='TP53',
            protein_name='Cellular tumor antigen p53',
            uniprot_id='P04637',
            description='Tumor suppressor',
        )
        self.protein2 = Protein.objects.create(
            gene_name='BRCA1',
            protein_name='Breast cancer type 1',
            uniprot_id='P38398',
            description='DNA repair',
        )

    def test_list_proteins(self):
        """GET /api/proteins/ should return a paginated list of proteins."""
        response = self.client.get('/api/proteins/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Pagination wraps results in a dict with 'results' key
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_protein(self):
        """GET /api/proteins/<id>/ should return a single protein."""
        response = self.client.get(f'/api/proteins/{self.protein.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['gene_name'], 'TP53')
        self.assertEqual(response.data['uniprot_id'], 'P04637')

    def test_create_protein(self):
        """POST /api/proteins/ should create a new protein."""
        data = {
            'gene_name': 'EGFR',
            'protein_name': 'Epidermal growth factor receptor',
            'uniprot_id': 'P00533',
            'ensembl_id': '',
            'entrez_id': '',
            'description': 'Receptor tyrosine kinase',
            'sequence': '',
        }
        response = self.client.post('/api/proteins/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Protein.objects.count(), 3)
        self.assertEqual(response.data['gene_name'], 'EGFR')

    def test_update_protein(self):
        """PUT /api/proteins/<id>/ should update an existing protein."""
        data = {
            'gene_name': 'TP53_UPDATED',
            'protein_name': 'Updated name',
            'uniprot_id': 'P04637',
            'ensembl_id': '',
            'entrez_id': '',
            'description': 'Updated',
            'sequence': '',
        }
        response = self.client.put(
            f'/api/proteins/{self.protein.pk}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.protein.refresh_from_db()
        self.assertEqual(self.protein.gene_name, 'TP53_UPDATED')

    def test_delete_protein(self):
        """DELETE /api/proteins/<id>/ should remove the protein."""
        response = self.client.delete(f'/api/proteins/{self.protein.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Protein.objects.count(), 1)

    def test_search_filter(self):
        """GET /api/proteins/?search=TP53 should filter results."""
        response = self.client.get('/api/proteins/', {'search': 'TP53'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['gene_name'], 'TP53')

    def test_ordering_filter(self):
        """GET /api/proteins/?ordering=-gene_name should order results."""
        response = self.client.get('/api/proteins/', {'ordering': '-gene_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [p['gene_name'] for p in response.data['results']]
        self.assertEqual(names, ['TP53', 'BRCA1'])

    def test_retrieve_nonexistent_returns_404(self):
        """GET /api/proteins/99999/ should return 404."""
        response = self.client.get('/api/proteins/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class InteractionViewSetTest(TestCase):
    """Tests for the InteractionViewSet API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.protein_a = Protein.objects.create(
            gene_name='TP53', uniprot_id='P04637',
        )
        self.protein_b = Protein.objects.create(
            gene_name='MDM2', uniprot_id='Q00987',
        )
        self.protein_c = Protein.objects.create(
            gene_name='BRCA1', uniprot_id='P38398',
        )
        self.interaction1 = Interaction.objects.create(
            protein_a=self.protein_a,
            protein_b=self.protein_b,
            score=0.99,
            interaction_type='physical',
            dataset='STRING',
        )
        self.interaction2 = Interaction.objects.create(
            protein_a=self.protein_a,
            protein_b=self.protein_c,
            score=0.87,
            interaction_type='physical',
            dataset='BioGRID',
        )

    def test_list_interactions(self):
        """GET /api/interactions/ should return a paginated list."""
        response = self.client.get('/api/interactions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_interaction_with_nested_proteins(self):
        """GET /api/interactions/<id>/ should return nested protein data."""
        response = self.client.get(f'/api/interactions/{self.interaction1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['protein_a'], dict)
        self.assertEqual(response.data['protein_a']['gene_name'], 'TP53')
        self.assertEqual(response.data['protein_b']['gene_name'], 'MDM2')

    def test_filter_by_protein_name(self):
        """GET /api/interactions/?protein=MDM2 should filter interactions."""
        response = self.client.get('/api/interactions/', {'protein': 'MDM2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        # Only interaction1 involves MDM2
        self.assertEqual(len(results), 1)

    def test_filter_returns_empty_for_nonmatching(self):
        """Filter with non-existing protein name should return empty list."""
        response = self.client.get('/api/interactions/', {'protein': 'ZZZZZZ'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_read_only_no_post(self):
        """POST /api/interactions/ should return 405 (read-only viewset)."""
        data = {
            'protein_a': self.protein_a.pk,
            'protein_b': self.protein_b.pk,
            'score': 0.5,
            'dataset': 'Test',
        }
        response = self.client.post('/api/interactions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_read_only_no_delete(self):
        """DELETE /api/interactions/<id>/ should return 405 (read-only viewset)."""
        response = self.client.delete(f'/api/interactions/{self.interaction1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class UploadViewTest(TestCase):
    """Tests for the UploadView (CSV/TSV file upload)."""

    def setUp(self):
        self.client = APIClient()
        self.protein_a = Protein.objects.create(
            gene_name='TP53', uniprot_id='P04637',
        )
        self.protein_b = Protein.objects.create(
            gene_name='MDM2', uniprot_id='Q00987',
        )

    def _make_csv(self, content, filename='test.csv'):
        """Helper to create an in-memory file for upload."""
        f = io.BytesIO(content.encode('utf-8'))
        f.name = filename
        return f

    def test_upload_valid_csv(self):
        """Upload a valid CSV should create interactions."""
        csv_content = "gene_a,gene_b,score,dataset\nTP53,MDM2,0.95,TestDB\n"
        f = self._make_csv(csv_content, 'data.csv')
        response = self.client.post('/api/upload/', {'file': f}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success_rows'], 1)
        self.assertEqual(len(response.data['errors']), 0)
        self.assertEqual(Interaction.objects.count(), 1)

    def test_upload_valid_tsv(self):
        """Upload a valid TSV should create interactions."""
        tsv_content = "P04637\tQ00987\n"
        f = self._make_csv(tsv_content, 'data.tsv')
        response = self.client.post('/api/upload/', {'file': f}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success_rows'], 1)

    def test_upload_no_file_returns_400(self):
        """POST /api/upload/ with no file should return 400."""
        response = self.client.post('/api/upload/', {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_upload_unsupported_extension_returns_400(self):
        """Upload with unsupported extension (.json) should return 400."""
        f = self._make_csv('{"a": 1}', 'data.json')
        response = self.client.post('/api/upload/', {'file': f}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_upload_csv_missing_columns_returns_400(self):
        """CSV missing required columns should return 400."""
        csv_content = "col_a,col_b\nTPP,MDM\n"
        f = self._make_csv(csv_content, 'bad.csv')
        response = self.client.post('/api/upload/', {'file': f}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_upload_csv_nonexistent_protein_reports_error(self):
        """CSV referencing non-existent proteins should report row errors."""
        csv_content = "gene_a,gene_b,score,dataset\nFAKE1,FAKE2,0.5,TestDB\n"
        f = self._make_csv(csv_content, 'missing.csv')
        response = self.client.post('/api/upload/', {'file': f}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success_rows'], 0)
        self.assertGreater(len(response.data['errors']), 0)

    def test_upload_duplicate_interaction_no_error(self):
        """Uploading same interaction twice should use get_or_create without error."""
        csv_content = "gene_a,gene_b,score,dataset\nTP53,MDM2,0.95,TestDB\n"
        f1 = self._make_csv(csv_content, 'data1.csv')
        self.client.post('/api/upload/', {'file': f1}, format='multipart')
        f2 = self._make_csv(csv_content, 'data2.csv')
        response = self.client.post('/api/upload/', {'file': f2}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only 1 interaction should exist (get_or_create doesn't duplicate)
        self.assertEqual(Interaction.objects.count(), 1)

    def test_upload_valid_txt_file(self):
        """Upload a valid .txt file (treated as TSV) should work."""
        txt_content = "P04637\tQ00987\n"
        f = self._make_csv(txt_content, 'data.txt')
        response = self.client.post('/api/upload/', {'file': f}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success_rows'], 1)
