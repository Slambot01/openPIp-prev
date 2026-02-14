import { useState } from 'react';
import {
  Container,
  Typography,
  TextField,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Box,
  CircularProgress,
  Alert,
  InputAdornment,
  Card,
  CardContent,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { proteinApi } from './api/proteinApi';
import type { Protein } from './api/proteinApi';

function App() {
  const [proteins, setProteins] = useState<Protein[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    setLoading(true);
    setError(null);

    try {
      const data = await proteinApi.searchProteins(query);
      setProteins(data.results);
    } catch (err) {
      setError('Failed to fetch proteins. Make sure Django server is running on http://127.0.0.1:8000');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4, textAlign: 'center', py: 3 }}>
        <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 600, color: '#2c3e50' }}>
          openPIP 2.0 Preview
        </Typography>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          Modern Protein Interaction Platform
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Django + React + TypeScript • GSoC 2026 Proof of Concept
        </Typography>
      </Box>

      {/* Search Box */}
      <Card sx={{ mb: 4, boxShadow: 3 }}>
        <CardContent>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Search proteins by gene name, UniProt ID, or description (e.g., TP53, BRCA1)"
            value={searchQuery}
            onChange={(e) => handleSearch(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
            sx={{ mb: 1 }}
          />
          <Typography variant="caption" color="text.secondary">
            {proteins.length} protein{proteins.length !== 1 ? 's' : ''} found
          </Typography>
        </CardContent>
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Loading Spinner */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {/* Results Table */}
      {!loading && proteins.length > 0 && (
        <TableContainer component={Paper} sx={{ boxShadow: 3 }}>
          <Table>
            <TableHead>
              <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                <TableCell sx={{ fontWeight: 'bold' }}>Gene Name</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Protein Name</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>UniProt ID</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Ensembl ID</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Description</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {proteins.map((protein) => (
                <TableRow
                  key={protein.id}
                  sx={{ '&:hover': { backgroundColor: '#f9f9f9' } }}
                >
                  <TableCell sx={{ fontWeight: 500, color: '#1976d2' }}>
                    {protein.gene_name}
                  </TableCell>
                  <TableCell>{protein.protein_name}</TableCell>
                  <TableCell>
                    <a
                      href={`https://www.uniprot.org/uniprotkb/${protein.uniprot_id}/entry`}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ color: '#1976d2', textDecoration: 'none' }}
                    >
                      {protein.uniprot_id}
                    </a>
                  </TableCell>
                  <TableCell>{protein.ensembl_id}</TableCell>
                  <TableCell sx={{ maxWidth: 300 }}>{protein.description}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Empty State */}
      {!loading && proteins.length === 0 && searchQuery === '' && (
        <Box sx={{ textAlign: 'center', py: 6 }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Start typing to search proteins
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Try searching for: TP53, BRCA1, EGFR, MYC, or KRAS
          </Typography>
        </Box>
      )}

      {/* No Results */}
      {!loading && proteins.length === 0 && searchQuery !== '' && (
        <Box sx={{ textAlign: 'center', py: 6 }}>
          <Typography variant="h6" color="text.secondary">
            No proteins found for "{searchQuery}"
          </Typography>
        </Box>
      )}
    </Container>
  );
}

export default App;
