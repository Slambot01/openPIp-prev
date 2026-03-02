import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import {
    Box, Typography, Paper, Button, CircularProgress,
    Alert, List, ListItem, ListItemText, Chip, Divider
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import { proteinApi } from '../api/proteinApi';
import type { UploadResponse } from '../api/proteinApi';

export default function UploadPage() {
    const [uploading, setUploading] = useState(false);
    const [result, setResult] = useState<UploadResponse | null>(null);
    const [uploadError, setUploadError] = useState<string | null>(null);
    const [fileName, setFileName] = useState<string | null>(null);

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        const file = acceptedFiles[0];
        if (!file) return;

        setFileName(file.name);
        setUploading(true);
        setResult(null);
        setUploadError(null);

        try {
            const data = await proteinApi.uploadFile(file);
            setResult(data);
        } catch (err: unknown) {
            const error = err as { response?: { data?: { error?: string } } };
            setUploadError(error?.response?.data?.error || 'Upload failed. Check Django server.');
        } finally {
            setUploading(false);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'text/csv': ['.csv'],
            'text/tab-separated-values': ['.tsv'],
            'text/plain': ['.txt'],
        },
        multiple: false,
    });

    return (
        <Box sx={{ p: 3, maxWidth: 800, mx: 'auto' }}>
            <Typography variant="h4" sx={{ fontWeight: 600, color: '#2c3e50', mb: 1 }}>
                Upload Interaction Data
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Upload a file to import protein-protein interactions into the database.
            </Typography>

            {/* Format Info */}
            <Paper sx={{ p: 2, mb: 3, backgroundColor: '#f8f9fa' }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>Supported Formats:</Typography>
                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                    <Box>
                        <Chip label=".csv" size="small" color="primary" sx={{ mb: 0.5 }} />
                        <Typography variant="caption" display="block" color="text.secondary">
                            Columns: gene_a, gene_b, score, dataset
                        </Typography>
                    </Box>
                    <Box>
                        <Chip label=".tsv / .txt" size="small" color="secondary" sx={{ mb: 0.5 }} />
                        <Typography variant="caption" display="block" color="text.secondary">
                            PSI-MI TAB: col0=UniProt_A, col1=UniProt_B
                        </Typography>
                    </Box>
                </Box>
            </Paper>

            {/* Drop Zone */}
            <Paper
                {...getRootProps()}
                sx={{
                    p: 6,
                    mb: 3,
                    textAlign: 'center',
                    border: '2px dashed',
                    borderColor: isDragActive ? '#1976d2' : '#ccc',
                    backgroundColor: isDragActive ? '#e3f2fd' : '#fafafa',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    '&:hover': { borderColor: '#1976d2', backgroundColor: '#e3f2fd' },
                }}
            >
                <input {...getInputProps()} />
                <UploadFileIcon sx={{ fontSize: 56, color: isDragActive ? '#1976d2' : '#aaa', mb: 2 }} />
                {isDragActive ? (
                    <Typography variant="h6" color="primary">Drop the file here...</Typography>
                ) : (
                    <>
                        <Typography variant="h6" color="text.secondary" gutterBottom>
                            Drag & drop a file here
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            or
                        </Typography>
                        <Button variant="contained" size="large">
                            Browse File
                        </Button>
                    </>
                )}
                {fileName && !uploading && (
                    <Typography variant="body2" sx={{ mt: 2, color: '#1976d2' }}>
                        Selected: {fileName}
                    </Typography>
                )}
            </Paper>

            {/* Loading */}
            {uploading && (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                    <CircularProgress size={24} />
                    <Typography>Uploading and parsing {fileName}...</Typography>
                </Box>
            )}

            {/* Upload Error */}
            {uploadError && (
                <Alert severity="error" sx={{ mb: 3 }}>
                    {uploadError}
                </Alert>
            )}

            {/* Results */}
            {result && (
                <Paper sx={{ p: 3 }}>
                    <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>Upload Results</Typography>

                    {/* Success count */}
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                        <CheckCircleIcon color="success" />
                        <Typography variant="body1" color="success.main" sx={{ fontWeight: 600 }}>
                            {result.success_rows} row{result.success_rows !== 1 ? 's' : ''} imported successfully
                        </Typography>
                    </Box>

                    {/* Errors */}
                    {result.errors.length > 0 && (
                        <>
                            <Divider sx={{ my: 2 }} />
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                                <ErrorIcon color="error" />
                                <Typography variant="body1" color="error" sx={{ fontWeight: 600 }}>
                                    {result.errors.length} error{result.errors.length !== 1 ? 's' : ''}
                                </Typography>
                            </Box>
                            <List dense>
                                {result.errors.map((err, idx) => (
                                    <ListItem key={idx} sx={{ py: 0.5, px: 0 }}>
                                        <ListItemText
                                            primary={
                                                <Typography variant="body2" color="error">
                                                    <strong>Row {err.row}:</strong> {err.message}
                                                </Typography>
                                            }
                                        />
                                    </ListItem>
                                ))}
                            </List>
                        </>
                    )}
                </Paper>
            )}
        </Box>
    );
}
