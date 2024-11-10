'use client';
import { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Chip,
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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Button,
} from '@mui/material';
import {
  KeyboardArrowDown,
  KeyboardArrowUp,
  Search as SearchIcon,
  FilterList as FilterIcon,
  BugReport,
  Security,
} from '@mui/icons-material';

interface Vulnerability {
  id: string;
  title: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  type: string;
  target: string;
  description: string;
  tool: string;
  timestamp: string;
  status: 'open' | 'in_progress' | 'resolved' | 'false_positive';
  aiRecommendations?: string[];
  details?: Record<string, any>;
}

function SeverityChip({ severity }: { severity: string }) {
  const colors: Record<string, any> = {
    critical: 'error',
    high: 'error',
    medium: 'warning',
    low: 'info',
    info: 'default',
  };

  return (
    <Chip
      label={severity.toUpperCase()}
      color={colors[severity]}
      size="small"
      sx={{ minWidth: 80 }}
    />
  );
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
        <TableCell align="center">
          <SeverityChip severity={vulnerability.severity} />
        </TableCell>
        <TableCell>{vulnerability.type}</TableCell>
        <TableCell>{vulnerability.target}</TableCell>
        <TableCell>{vulnerability.tool}</TableCell>
        <TableCell>
          <Chip
            label={vulnerability.status.replace('_', ' ').toUpperCase()}
            color={
              vulnerability.status === 'resolved'
                ? 'success'
                : vulnerability.status === 'in_progress'
                ? 'warning'
                : vulnerability.status === 'false_positive'
                ? 'default'
                : 'error'
            }
            size="small"
          />
        </TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={7}>
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
                        severity="info"
                        sx={{ mb: 1 }}
                        icon={<Security />}
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
  const [filters, setFilters] = useState({
    severity: 'all',
    status: 'all',
    search: '',
  });

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
    const matchesSeverity =
      filters.severity === 'all' || vuln.severity === filters.severity;
    const matchesStatus =
      filters.status === 'all' || vuln.status === filters.status;
    const matchesSearch =
      filters.search === '' ||
      vuln.title.toLowerCase().includes(filters.search.toLowerCase()) ||
      vuln.description.toLowerCase().includes(filters.search.toLowerCase());

    return matchesSeverity && matchesStatus && matchesSearch;
  });

  const handleExport = () => {
    const exportData = filteredVulnerabilities.map((vuln) => ({
      ...vuln,
      severity: vuln.severity.toUpperCase(),
      status: vuln.status.replace('_', ' ').toUpperCase(),
    }));

    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
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
              <Grid item xs={12} sm={4}>
                <TextField
                  fullWidth
                  label="Search"
                  value={filters.search}
                  onChange={(e) =>
                    setFilters({ ...filters, search: e.target.value })
                  }
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon />
                      </InputAdornment>
                    ),
                  }}
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <FormControl fullWidth>
                  <InputLabel>Severity</InputLabel>
                  <Select
                    value={filters.severity}
                    label="Severity"
                    onChange={(e) =>
                      setFilters({ ...filters, severity: e.target.value })
                    }
                    startAdornment={
                      <InputAdornment position="start">
                        <FilterIcon />
                      </InputAdornment>
                    }
                  >
                    <MenuItem value="all">All Severities</MenuItem>
                    <MenuItem value="critical">Critical</MenuItem>
                    <MenuItem value="high">High</MenuItem>
                    <MenuItem value="medium">Medium</MenuItem>
                    <MenuItem value="low">Low</MenuItem>
                    <MenuItem value="info">Info</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={4}>
                <FormControl fullWidth>
                  <InputLabel>Status</InputLabel>
                  <Select
                    value={filters.status}
                    label="Status"
                    onChange={(e) =>
                      setFilters({ ...filters, status: e.target.value })
                    }
                  >
                    <MenuItem value="all">All Statuses</MenuItem>
                    <MenuItem value="open">Open</MenuItem>
                    <MenuItem value="in_progress">In Progress</MenuItem>
                    <MenuItem value="resolved">Resolved</MenuItem>
                    <MenuItem value="false_positive">False Positive</MenuItem>
                  </Select>
                </FormControl>
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
                    <TableCell align="center">Severity</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Target</TableCell>
                    <TableCell>Tool</TableCell>
                    <TableCell>Status</TableCell>
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
