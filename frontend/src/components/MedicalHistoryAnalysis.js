import React from 'react';
import { Card, Typography, List, ListItem, ListItemIcon, ListItemText, Divider, Box, Alert } from '@mui/material';
import {
  MedicalServices,
  Warning,
  CheckCircle,
  Info,
  LocalHospital,
  MonitorHeart,
  Psychology,
  FitnessCenter,
  Restaurant,
  Spa
} from '@mui/icons-material';

const MedicalHistoryAnalysis = ({ analysis }) => {
  console.log('Received analysis in component:', analysis);

  if (!analysis) {
    return (
      <Alert severity="error">
        No analysis data available. Please try again.
      </Alert>
    );
  }

  // Extract the analysis text - handle both string and object formats
  const analysisText = typeof analysis === 'string' ? analysis : 
                      analysis.analysis ? analysis.analysis :
                      analysis.diagnosis ? analysis.diagnosis.analysis : 
                      'Analysis not available';

  return (
    <Box sx={{ mt: 4 }}>
      <Card sx={{ p: 3, mb: 3, backgroundColor: '#f8f9fa', boxShadow: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ color: '#34495e', display: 'flex', alignItems: 'center', gap: 1 }}>
          <MedicalServices sx={{ color: '#3498db' }} />
          Analysis Results
        </Typography>
        <Typography variant="body1" sx={{ color: '#2c3e50', mt: 2, whiteSpace: 'pre-wrap' }}>
          {analysisText}
        </Typography>
      </Card>

      {/* Display additional sections if available */}
      {analysis.recommendations && (
        <Card sx={{ p: 3, mb: 3, backgroundColor: '#f8f9fa', boxShadow: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ color: '#34495e', mb: 2 }}>
            Recommendations
          </Typography>
          <List>
            {Object.entries(analysis.recommendations).map(([key, value], index) => (
              <React.Fragment key={key}>
                <ListItem>
                  <ListItemIcon sx={{ color: '#2ecc71' }}>
                    {key === 'diet' ? <Restaurant /> : 
                     key === 'exercise' ? <FitnessCenter /> : 
                     key === 'stress' ? <Spa /> : 
                     <Info />}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Typography variant="subtitle1" sx={{ fontWeight: 'bold', color: '#2c3e50' }}>
                        {key.charAt(0).toUpperCase() + key.slice(1)} Recommendations
                      </Typography>
                    }
                    secondary={
                      <Typography variant="body2" sx={{ color: '#34495e', mt: 1 }}>
                        {value}
                      </Typography>
                    }
                  />
                </ListItem>
                {index < Object.entries(analysis.recommendations).length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Card>
      )}

      <Card sx={{ p: 3, mt: 3, backgroundColor: '#f8f9fa', boxShadow: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ color: '#34495e', display: 'flex', alignItems: 'center', gap: 1 }}>
          <Warning sx={{ color: '#e74c3c' }} />
          Important Notes
        </Typography>
        <List>
          <ListItem>
            <ListItemText
              primary={
                <Typography variant="body1" sx={{ color: '#2c3e50' }}>
                  • This is an AI-generated preliminary analysis and should not replace professional medical evaluation
                </Typography>
              }
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary={
                <Typography variant="body1" sx={{ color: '#2c3e50' }}>
                  • Seek immediate medical attention if symptoms worsen or new symptoms develop
                </Typography>
              }
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary={
                <Typography variant="body1" sx={{ color: '#2c3e50' }}>
                  • Regular follow-up with healthcare providers is essential
                </Typography>
              }
            />
          </ListItem>
        </List>
      </Card>
    </Box>
  );
};

export default MedicalHistoryAnalysis; 