import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

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

export interface Interaction {
  id: number;
  protein_a: Protein;
  protein_b: Protein;
  score: number;
  interaction_type: string;
  dataset: string;
  created_at: string;
}

export interface InteractionListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Interaction[];
}

export interface UploadResponse {
  success_rows: number;
  errors: { row: number; message: string }[];
}

export const proteinApi = {
  searchProteins: async (query: string = ''): Promise<ProteinListResponse> => {
    const response = await axios.get<ProteinListResponse>(`${API_BASE_URL}/proteins/`, {
      params: { search: query },
    });
    return response.data;
  },

  getProtein: async (id: number): Promise<Protein> => {
    const response = await axios.get<Protein>(`${API_BASE_URL}/proteins/${id}/`);
    return response.data;
  },

  fetchInteractions: async (protein: string): Promise<Interaction[]> => {
    const response = await axios.get<InteractionListResponse>(`${API_BASE_URL}/interactions/`, {
      params: { protein },
    });
    return response.data.results;
  },

  uploadFile: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post<UploadResponse>(`${API_BASE_URL}/upload/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
};

