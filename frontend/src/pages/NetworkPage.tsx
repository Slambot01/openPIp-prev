import { useEffect, useRef, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import {
    Box, TextField, Typography, Paper, CircularProgress,
    Alert, Button, ButtonGroup, Tooltip, Chip
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import InputAdornment from '@mui/material/InputAdornment';
import DownloadIcon from '@mui/icons-material/Download';
import cytoscape from 'cytoscape';
import { proteinApi } from '../api/proteinApi';
import type { Interaction } from '../api/proteinApi';

const LAYOUT_OPTIONS = {
    cose: {
        name: 'cose',
        animate: true,
        randomize: false,
        nodeRepulsion: () => 400000,
        idealEdgeLength: () => 120,
        edgeElasticity: () => 100,
    },
    circle: {
        name: 'circle',
        animate: true,
        padding: 40,
    },
};

export default function NetworkPage() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const cyRef = useRef<HTMLDivElement>(null);
    const cyInstance = useRef<cytoscape.Core | null>(null);

    const [query, setQuery] = useState(searchParams.get('protein') || '');
    const [inputVal, setInputVal] = useState(searchParams.get('protein') || '');
    const [interactions, setInteractions] = useState<Interaction[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [layout, setLayout] = useState<'cose' | 'circle'>('cose');
    const [tooltip, setTooltip] = useState<{
        gene: string; uniprot: string; x: number; y: number
    } | null>(null);

    // Fetch on query change
    useEffect(() => {
        if (!query) return;
        const fetchData = async () => {
            setLoading(true);
            setError(null);
            try {
                const data = await proteinApi.fetchInteractions(query);
                setInteractions(data);
            } catch {
                setError('Failed to fetch interactions. Make sure Django server is running.');
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [query]);

    // Build Cytoscape graph
    useEffect(() => {
        if (!cyRef.current || loading) return;

        if (cyInstance.current) {
            cyInstance.current.destroy();
        }

        if (interactions.length === 0) return;

        // Build unique nodes
        const nodeMap = new Map<number, { gene: string; uniprot: string }>();
        interactions.forEach(i => {
            nodeMap.set(i.protein_a.id, { gene: i.protein_a.gene_name, uniprot: i.protein_a.uniprot_id });
            nodeMap.set(i.protein_b.id, { gene: i.protein_b.gene_name, uniprot: i.protein_b.uniprot_id });
        });

        const nodes = Array.from(nodeMap.entries()).map(([id, data]) => ({
            data: { id: `p${id}`, label: data.gene, uniprot: data.uniprot },
        }));

        const edges = interactions.map(i => ({
            data: {
                id: `e${i.id}`,
                source: `p${i.protein_a.id}`,
                target: `p${i.protein_b.id}`,
                score: i.score,
                type: i.interaction_type,
                dataset: i.dataset,
            },
        }));

        const cy = cytoscape({
            container: cyRef.current,
            elements: { nodes, edges },
            style: [
                {
                    selector: 'node',
                    style: {
                        'background-color': '#1976d2',
                        'label': 'data(label)',
                        'color': '#fff',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'font-size': '12px',
                        'font-weight': 'bold',
                        'width': '60px',
                        'height': '60px',
                        'border-width': 2,
                        'border-color': '#0d47a1',
                    },
                },
                {
                    selector: 'node:selected',
                    style: {
                        'background-color': '#e91e63',
                        'border-color': '#880e4f',
                    },
                },
                {
                    selector: 'edge',
                    style: {
                        'width': (ele: cytoscape.EdgeSingular) => Math.max(1, ele.data('score') * 6),
                        'line-color': '#90caf9',
                        'target-arrow-color': '#90caf9',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'bezier',
                        'label': (ele: cytoscape.EdgeSingular) => ele.data('score').toFixed(2),
                        'font-size': '10px',
                        'color': '#555',
                        'text-rotation': 'autorotate',
                    },
                },
                {
                    selector: 'edge:selected',
                    style: {
                        'line-color': '#e91e63',
                        'target-arrow-color': '#e91e63',
                    },
                },
            ],
            layout: LAYOUT_OPTIONS[layout],
        });

        // Node click tooltip
        cy.on('tap', 'node', (evt) => {
            const node = evt.target;
            const pos = node.renderedPosition();
            setTooltip({
                gene: node.data('label'),
                uniprot: node.data('uniprot'),
                x: pos.x,
                y: pos.y,
            });
        });

        cy.on('tap', (evt) => {
            if (evt.target === cy) setTooltip(null);
        });

        cyInstance.current = cy;

        return () => {
            cy.destroy();
        };
    }, [interactions, loading, layout]);

    const handleSearch = () => {
        setQuery(inputVal);
        navigate(`/network?protein=${inputVal}`);
    };

    const handleLayoutChange = (newLayout: 'cose' | 'circle') => {
        setLayout(newLayout);
        if (cyInstance.current) {
            cyInstance.current.layout(LAYOUT_OPTIONS[newLayout]).run();
        }
    };

    const handleDownloadPNG = () => {
        if (!cyInstance.current) return;
        const png = cyInstance.current.png({ output: 'blob', bg: 'white', full: true, scale: 2 });
        const url = URL.createObjectURL(png as Blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${query}_network.png`;
        a.click();
        URL.revokeObjectURL(url);
    };

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" sx={{ fontWeight: 600, color: '#2c3e50', mb: 1 }}>
                Network Visualization
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Search a protein to see its interaction network
            </Typography>

            {/* Search */}
            <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
                <TextField
                    fullWidth
                    variant="outlined"
                    placeholder="Enter gene name (e.g., TP53, BRCA1)"
                    value={inputVal}
                    onChange={(e) => setInputVal(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                    InputProps={{
                        startAdornment: (
                            <InputAdornment position="start">
                                <SearchIcon />
                            </InputAdornment>
                        ),
                    }}
                />
                <Button variant="contained" onClick={handleSearch} sx={{ px: 4 }}>
                    Search
                </Button>
            </Box>

            {/* Layout toggle */}
            {interactions.length > 0 && (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                    <Typography variant="body2" color="text.secondary">Layout:</Typography>
                    <ButtonGroup size="small">
                        <Button
                            variant={layout === 'cose' ? 'contained' : 'outlined'}
                            onClick={() => handleLayoutChange('cose')}
                        >
                            CoSE
                        </Button>
                        <Button
                            variant={layout === 'circle' ? 'contained' : 'outlined'}
                            onClick={() => handleLayoutChange('circle')}
                        >
                            Circle
                        </Button>
                    </ButtonGroup>
                    <Chip label={`${interactions.length} interactions`} size="small" color="primary" />
                    <Button
                        size="small"
                        variant="outlined"
                        startIcon={<DownloadIcon />}
                        onClick={handleDownloadPNG}
                        sx={{ ml: 'auto' }}
                    >
                        Download PNG
                    </Button>
                </Box>
            )}

            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

            {loading && (
                <Box sx={{ display: 'flex', justifyContent: 'center', my: 6 }}>
                    <CircularProgress />
                </Box>
            )}

            {/* Cytoscape container */}
            {!loading && interactions.length > 0 && (
                <Paper sx={{ position: 'relative', height: '60vh', boxShadow: 3 }}>
                    <div ref={cyRef} style={{ width: '100%', height: '100%' }} />
                    {tooltip && (
                        <Tooltip title="" open placement="top">
                            <Paper
                                elevation={4}
                                sx={{
                                    position: 'absolute',
                                    left: tooltip.x,
                                    top: tooltip.y - 80,
                                    transform: 'translateX(-50%)',
                                    p: 1.5,
                                    pointerEvents: 'none',
                                    zIndex: 10,
                                    minWidth: 140,
                                }}
                            >
                                <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>{tooltip.gene}</Typography>
                                <Typography variant="caption" color="text.secondary">{tooltip.uniprot}</Typography>
                            </Paper>
                        </Tooltip>
                    )}
                </Paper>
            )}

            {!loading && interactions.length === 0 && query && (
                <Box sx={{ textAlign: 'center', py: 6 }}>
                    <Typography variant="h6" color="text.secondary">
                        No interactions found for "{query}"
                    </Typography>
                </Box>
            )}

            {!query && (
                <Box sx={{ textAlign: 'center', py: 6 }}>
                    <Typography variant="h6" color="text.secondary">
                        Search for a protein to see its interaction network
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Try: TP53, BRCA1, EGFR, MYC, KRAS
                    </Typography>
                </Box>
            )}
        </Box>
    );
}
