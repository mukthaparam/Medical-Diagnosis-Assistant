import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  CircularProgress,
  Alert,
  Stepper,
  Step,
  StepLabel,
  Card,
  CardContent,
  Grid,
  Chip,
  IconButton,
  Tooltip,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import MedicalHistoryAnalysis from './MedicalHistoryAnalysis';

const Diagnosis = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [symptoms, setSymptoms] = useState(['']);
  const [patientInfo, setPatientInfo] = useState({
    age: '',
    gender: '',
    medical_history: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const steps = ['Patient Information', 'Symptoms', 'Analysis'];

  const handleNext = () => {
    if (activeStep === steps.length - 2) {
      handleSubmit();
    } else {
      setActiveStep((prevStep) => prevStep + 1);
    }
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
    if (activeStep === steps.length - 1) {
      setResult(null);
      setError(null);
    }
  };

  const handleSymptomChange = (index, value) => {
    const newSymptoms = [...symptoms];
    newSymptoms[index] = value;
    setSymptoms(newSymptoms);
  };

  const addSymptom = () => {
    setSymptoms([...symptoms, '']);
  };

  const removeSymptom = (index) => {
    const newSymptoms = symptoms.filter((_, i) => i !== index);
    setSymptoms(newSymptoms);
  };

  const handlePatientInfoChange = (field, value) => {
    setPatientInfo(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    try {
      console.log('Sending request with:', {
        symptoms: symptoms.filter(s => s.trim() !== ''),
        patient_info: patientInfo
      });

      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symptoms: symptoms.filter(s => s.trim() !== ''),
          patient_info: patientInfo
        }),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to analyze symptoms');
      }

      console.log('Received analysis result:', data);
      setResult(data);
      setActiveStep((prevStep) => prevStep + 1);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Box sx={{ mt: 2 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  label="Age"
                  type="number"
                  value={patientInfo.age}
                  onChange={(e) => handlePatientInfoChange('age', e.target.value)}
                  required
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <FormControl fullWidth required>
                  <InputLabel>Gender</InputLabel>
                  <Select
                    value={patientInfo.gender}
                    label="Gender"
                    onChange={(e) => handlePatientInfoChange('gender', e.target.value)}
                  >
                    <MenuItem value="">Select Gender</MenuItem>
                    <MenuItem value="male">Male</MenuItem>
                    <MenuItem value="female">Female</MenuItem>
                    <MenuItem value="other">Other</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Medical History"
                  multiline
                  rows={4}
                  value={patientInfo.medical_history}
                  onChange={(e) => handlePatientInfoChange('medical_history', e.target.value)}
                  placeholder="Please provide any relevant medical history, including chronic conditions, allergies, medications, etc."
                />
              </Grid>
            </Grid>
          </Box>
        );

      case 1:
        return (
          <Box sx={{ mt: 2 }}>
            {symptoms.map((symptom, index) => (
              <Box key={index} sx={{ display: 'flex', gap: 1, mb: 2 }}>
                <TextField
                  fullWidth
                  label={`Symptom ${index + 1}`}
                  value={symptom}
                  onChange={(e) => handleSymptomChange(index, e.target.value)}
                  placeholder="Describe your symptom"
                />
                {symptoms.length > 1 && (
                  <Tooltip title="Remove Symptom">
                    <IconButton
                      color="error"
                      onClick={() => removeSymptom(index)}
                      sx={{ mt: 1 }}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                )}
              </Box>
            ))}
            <Button
              startIcon={<AddIcon />}
              onClick={addSymptom}
              sx={{ mt: 2 }}
            >
              Add Another Symptom
            </Button>
          </Box>
        );

      case 2:
        return (
          <Box sx={{ mt: 2 }}>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                <CircularProgress />
              </Box>
            ) : error ? (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
                <br />
                Please try again or contact support if the problem persists.
              </Alert>
            ) : result ? (
              <>
                <Alert severity="info" sx={{ mb: 2 }}>
                  Analysis completed successfully
                </Alert>
                <MedicalHistoryAnalysis analysis={result} />
              </>
            ) : (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                <Typography>Click Analyze to process your symptoms</Typography>
              </Box>
            )}
          </Box>
        );

      default:
        return null;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4, borderRadius: 2 }}>
        <Typography variant="h4" gutterBottom sx={{ color: '#2c3e50', fontWeight: 'bold' }}>
          Medical Diagnosis Assistant
        </Typography>

        <Stepper activeStep={activeStep} sx={{ mt: 4, mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {renderStepContent(activeStep)}

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button
            variant="outlined"
            onClick={handleBack}
            disabled={activeStep === 0}
            sx={{ color: '#2c3e50', borderColor: '#2c3e50' }}
          >
            Back
          </Button>
          <Button
            variant="contained"
            onClick={handleNext}
            disabled={
              loading ||
              (activeStep === 0 && (!patientInfo.age || !patientInfo.gender)) ||
              (activeStep === 1 && symptoms.filter(s => s.trim() !== '').length === 0)
            }
            sx={{
              backgroundColor: '#3498db',
              '&:hover': {
                backgroundColor: '#2980b9'
              }
            }}
          >
            {activeStep === steps.length - 1 ? 'Done' : 'Next'}
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default Diagnosis; 