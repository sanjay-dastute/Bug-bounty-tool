'use client';
import { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  TextField,
  Button,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Stepper,
  Step,
  StepLabel,
  CircularProgress,
  Alert,
  SelectChangeEvent,
} from '@mui/material';

const scanTypes = [
  { value: 'web', label: 'Web Application', tools: ['Nmap', 'Nuclei'] },
  { value: 'mobile', label: 'Mobile Application', tools: ['MobSF'] },
  { value: 'api', label: 'API Endpoint', tools: ['Nuclei'] },
  { value: 'source', label: 'Source Code', tools: ['Static Analysis'] },
  { value: 'smart-contract', label: 'Smart Contract', tools: ['Mythril'] },
  { value: 'blockchain', label: 'Blockchain', tools: ['Custom Analysis'] },
];

const steps = ['Select Scan Type', 'Configure Options', 'Review & Start'];

export default function ScanPage() {
  const [activeStep, setActiveStep] = useState(0);
  const [scanType, setScanType] = useState('');
  const [target, setTarget] = useState('');
  const [selectedTools, setSelectedTools] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [scanOptions, setScanOptions] = useState({
    depth: 'normal',
    timeout: '300',
    concurrent: '10',
  });

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleScanTypeChange = (event: SelectChangeEvent<string>) => {
    const type = event.target.value;
    setScanType(type);
    const tools = scanTypes.find(t => t.value === type)?.tools || [];
    setSelectedTools(tools);
  };

  const handleToolsChange = (event: SelectChangeEvent<string[]>) => {
    const tools = typeof event.target.value === 'string'
      ? event.target.value.split(',')
      : event.target.value;
    setSelectedTools(tools);
  };

  const handleStartScan = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('/api/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          scanType,
          target,
          tools: selectedTools,
          options: scanOptions,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to start scan');
      }

      const result = await response.json();
      // Redirect to scan results page
      window.location.href = `/scan/${result.scanId}`;

    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Scan Type</InputLabel>
                <Select
                  value={scanType}
                  label="Scan Type"
                  onChange={handleScanTypeChange}
                >
                  {scanTypes.map((type) => (
                    <MenuItem key={type.value} value={type.value}>
                      {type.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            {scanType && (
              <Grid item xs={12}>
                <Typography variant="body2" color="text.secondary">
                  {scanType === 'web' && 'Scan websites for vulnerabilities using Nmap and Nuclei'}
                  {scanType === 'mobile' && 'Analyze mobile applications (APK/IPA) for security issues'}
                  {scanType === 'api' && 'Test API endpoints for security vulnerabilities'}
                  {scanType === 'source' && 'Analyze source code for security flaws'}
                  {scanType === 'smart-contract' && 'Audit smart contracts using Mythril'}
                  {scanType === 'blockchain' && 'Analyze blockchain networks and transactions'}
                </Typography>
              </Grid>
            )}
          </Grid>
        );
      case 1:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Target"
                value={target}
                onChange={(e) => setTarget(e.target.value)}
                placeholder={
                  scanType === 'web' ? 'Enter URL (e.g., https://example.com)' :
                  scanType === 'mobile' ? 'Upload APK/IPA file or enter URL' :
                  scanType === 'api' ? 'Enter API endpoint URL' :
                  scanType === 'source' ? 'Enter repository URL or upload files' :
                  scanType === 'smart-contract' ? 'Enter contract address or upload file' :
                  'Enter target'
                }
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Selected Tools</InputLabel>
                <Select
                  multiple
                  value={selectedTools}
                  label="Selected Tools"
                  onChange={handleToolsChange}
                >
                  {scanTypes
                    .find(t => t.value === scanType)
                    ?.tools.map((tool) => (
                      <MenuItem key={tool} value={tool}>
                        {tool}
                      </MenuItem>
                    ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth>
                <InputLabel>Scan Depth</InputLabel>
                <Select
                  value={scanOptions.depth}
                  label="Scan Depth"
                  onChange={(e) => setScanOptions({...scanOptions, depth: e.target.value})}
                >
                  <MenuItem value="quick">Quick</MenuItem>
                  <MenuItem value="normal">Normal</MenuItem>
                  <MenuItem value="deep">Deep</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                type="number"
                label="Timeout (seconds)"
                value={scanOptions.timeout}
                onChange={(e) => setScanOptions({...scanOptions, timeout: e.target.value})}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                type="number"
                label="Concurrent Scans"
                value={scanOptions.concurrent}
                onChange={(e) => setScanOptions({...scanOptions, concurrent: e.target.value})}
              />
            </Grid>
          </Grid>
        );
      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Scan Configuration Summary
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Typography>
                  <strong>Type:</strong> {scanTypes.find(t => t.value === scanType)?.label}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography>
                  <strong>Target:</strong> {target}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography>
                  <strong>Tools:</strong> {selectedTools.join(', ')}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography>
                  <strong>Options:</strong>
                </Typography>
                <Typography variant="body2" sx={{ ml: 2 }}>
                  • Scan Depth: {scanOptions.depth}
                  <br />
                  • Timeout: {scanOptions.timeout} seconds
                  <br />
                  • Concurrent Scans: {scanOptions.concurrent}
                </Typography>
              </Grid>
            </Grid>
          </Box>
        );
      default:
        return null;
    }
  };

  return (
    <Box sx={{ maxWidth: 800, margin: '0 auto', py: 4 }}>
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            New Vulnerability Scan
          </Typography>

          <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box sx={{ mb: 4 }}>
            {renderStepContent(activeStep)}
          </Box>

          <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
            <Button
              disabled={activeStep === 0}
              onClick={handleBack}
              sx={{ mr: 1 }}
            >
              Back
            </Button>
            {activeStep === steps.length - 1 ? (
              <Button
                variant="contained"
                onClick={handleStartScan}
                disabled={loading || !scanType || !target || selectedTools.length === 0}
              >
                {loading ? (
                  <CircularProgress size={24} sx={{ mr: 1 }} />
                ) : null}
                Start Scan
              </Button>
            ) : (
              <Button
                variant="contained"
                onClick={handleNext}
                disabled={!scanType || (activeStep === 1 && !target)}
              >
                Next
              </Button>
            )}
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}
