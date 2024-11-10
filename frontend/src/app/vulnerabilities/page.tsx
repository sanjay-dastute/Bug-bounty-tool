'use client';
import { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Collapse,
  TextField,
  InputAdornment,
  Alert,
  CircularProgress,
  Button,
} from '@mui/material';
import {
  KeyboardArrowDown,
  KeyboardArrowUp,
  Search as SearchIcon,
  BugReport,
  Security,
} from '@mui/icons-material';

interface Vulnerability {
  id: string;
  title: string;
  type: string;
  target: string;
  description: string;
  tool: string;
  timestamp: string;
  details?: Record<string, any>;
  aiRecommendations?: string[];
}

function VulnerabilityRow({ vulnerability }: { vulnerability: Vulnerability }) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>
        <TableCell>
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUp /> : <KeyboardArrowDown />}
          </IconButton>
        </TableCell>
        <TableCell component="th" scope="row">
          {vulnerability.title}
        </TableCell>
        <TableCell>{vulnerability.type}</TableCell>
        <TableCell>{vulnerability.target}</TableCell>
        <TableCell>{vulnerability.tool}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={5}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 2 }}>
              <Typography variant="h6" gutterBottom component="div">
                Details
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="body1" paragraph>
                    {vulnerability.description}
                  </Typography>
                </Grid>
                {vulnerability.aiRecommendations && (
                  <Grid item xs={12}>
                    <Typography variant="subtitle1" gutterBottom>
                      AI Recommendations
                    </Typography>
                    {vulnerability.aiRecommendations.map((rec, index) => (
                      <Alert
                        key={index}
                        icon={<Security />}
                        sx={{ mb: 1 }}
                      >
                        {rec}
                      </Alert>
                    ))}
                  </Grid>
                )}
                {vulnerability.details && (
                  <Grid item xs={12}>
                    <Typography variant="subtitle1" gutterBottom>
                      Technical Details
                    </Typography>
                    <Paper variant="outlined" sx={{ p: 2 }}>
                      <pre style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
                        {JSON.stringify(vulnerability.details, null, 2)}
                      </pre>
                    </Paper>
                  </Grid>
                )}
              </Grid>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
}

export default function VulnerabilitiesPage() {
  const [vulnerabilities, setVulnerabilities] = useState<Vulnerability[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchFilter, setSearchFilter] = useState('');

  useEffect(() => {
    fetchVulnerabilities();
  }, []);

  const fetchVulnerabilities = async () => {
    try {
      const response = await fetch('/api/vulnerabilities');
      if (!response.ok) {
        throw new Error('Failed to fetch vulnerabilities');
      }
      const data = await response.json();
      setVulnerabilities(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const filteredVulnerabilities = vulnerabilities.filter((vuln) => {
    const matchesSearch =
      searchFilter === '' ||
      vuln.title.toLowerCase().includes(searchFilter.toLowerCase()) ||
      vuln.description.toLowerCase().includes(searchFilter.toLowerCase());

    return matchesSearch;
  });

  const handleExport = () => {
    const blob = new Blob([JSON.stringify(filteredVulnerabilities, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `vulnerabilities-${new Date().toISOString()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h5" component="h1">
              Vulnerabilities
            </Typography>
            <Button
              variant="contained"
              startIcon={<BugReport />}
              onClick={handleExport}
            >
              Export Report
            </Button>
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2, mb: 3 }}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Search"
                  value={searchFilter}
                  onChange={(e) => setSearchFilter(e.target.value)}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon />
                      </InputAdornment>
                    ),
                  }}
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
              <CircularProgress />
            </Box>
          ) : error ? (
            <Alert severity="error">{error}</Alert>
          ) : (
            <TableContainer component={Paper}>
              <Table aria-label="vulnerabilities table">
                <TableHead>
                  <TableRow>
                    <TableCell />
                    <TableCell>Title</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Target</TableCell>
                    <TableCell>Tool</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredVulnerabilities.map((vulnerability) => (
                    <VulnerabilityRow
                      key={vulnerability.id}
                      vulnerability={vulnerability}
                    />
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Grid>
      </Grid>
    </Box>
  );
}
