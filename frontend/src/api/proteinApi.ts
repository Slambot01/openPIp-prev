import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

export interface Protein {
  id: number;
  gene_name: string;
  protein_name: string;
  uniprot_id: string;
  ensembl_id: string;
  entrez_id: string;
  description: string;
  sequence: string;
  created_at: string;
  updated_at: string;
}

export interface ProteinListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Protein[];
}

export const proteinApi = {
  // Search proteins
  searchProteins: async (query: string = ''): Promise<ProteinListResponse> => {
    const response = await axios.get<ProteinListResponse>(`${API_BASE_URL}/proteins/`, {
      params: { search: query },
    });
    return response.data;
  },

  // Get single protein
  getProtein: async (id: number): Promise<Protein> => {
    const response = await axios.get<Protein>(`${API_BASE_URL}/proteins/${id}/`);
    return response.data;
  },
};
