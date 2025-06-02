import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Alert,
  useTheme,
  alpha,
  keyframes,
  IconButton
} from '@mui/material';
import { motion } from 'framer-motion';
import axios from 'axios';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CloseIcon from '@mui/icons-material/Close';

// Animation keyframes
const gradientAnimation = keyframes`
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
`;

const floatAnimation = keyframes`
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0px);
  }
`;

const pulseAnimation = keyframes`
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
`;

const FileUpload = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    handleFile(file);
  };

  const handleFile = (file) => {
    setError('');
    setSuccess('');

    if (!file) {
      return;
    }

    // Check file size (20MB = 20 * 1024 * 1024 bytes)
    if (file.size > 20 * 1024 * 1024) {
      setError('File size must not exceed 20MB');
      setSelectedFile(null);
      return;
    }

    // Check file extension
    if (!file.name.endsWith('.xlsx')) {
      setError('Only .xlsx files are allowed');
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setIsUploading(true);
    setError('');
    setSuccess('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await axios.post('http://localhost:5000/api/upload-file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSuccess('File uploaded successfully!');
      setSelectedFile(null);
      document.getElementById('file-input').value = '';
    } catch (error) {
      setError(error.response?.data?.error || 'Error uploading file');
      setSuccess('');
    } finally {
      setIsUploading(false);
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    document.getElementById('file-input').value = '';
  };

  const handleBackClick = () => {
    navigate('/survey');
  };

  const handleAnalysisClick = () => {
    navigate('/analysis');
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: `linear-gradient(-45deg, 
          ${alpha(theme.palette.primary.main, 0.1)}, 
          ${alpha(theme.palette.primary.dark, 0.2)}, 
          ${alpha(theme.palette.primary.main, 0.15)}, 
          ${alpha(theme.palette.primary.dark, 0.1)})`,
        backgroundSize: '400% 400%',
        animation: `${gradientAnimation} 15s ease infinite`,
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Animated Background Elements */}
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '100%',
          height: '100%',
          zIndex: 0,
          opacity: 0.1,
          background: `radial-gradient(circle at center, ${theme.palette.primary.main} 0%, transparent 70%)`,
          animation: `${floatAnimation} 6s ease-in-out infinite`
        }}
      />

      {/* Navigation Buttons */}
      <Box sx={{ position: 'absolute', top: 40, left: 40, right: 40, zIndex: 1, display: 'flex', justifyContent: 'space-between' }}>
        <Button
          variant="outlined"
          onClick={handleBackClick}
          sx={{
            borderRadius: 2,
            px: 3,
            py: 1,
            borderWidth: 2,
            bgcolor: alpha(theme.palette.background.paper, 0.7),
            borderColor: alpha(theme.palette.primary.main, 0.5),
            '&:hover': {
              borderWidth: 2,
              bgcolor: alpha(theme.palette.primary.main, 0.1)
            }
          }}
        >
          Back to Survey
        </Button>
        
        {success && (
          <Button
            variant="contained"
            onClick={handleAnalysisClick}
            sx={{
              borderRadius: 2,
              px: 4,
              py: 1.5,
              background: `linear-gradient(45deg, ${theme.palette.success.main}, ${theme.palette.success.dark})`,
              '&:hover': {
                background: `linear-gradient(45deg, ${theme.palette.success.dark}, ${theme.palette.success.main})`
              }
            }}
          >
            Student Learning Skills Analysis
          </Button>
        )}
      </Box>

      <Container maxWidth="md" sx={{ py: 4, position: 'relative', zIndex: 1, mt: 12 }}>
        <Paper 
          elevation={3} 
          sx={{ 
            p: 4, 
            borderRadius: 2,
            background: `linear-gradient(145deg, ${alpha(theme.palette.background.paper, 0.9)}, ${alpha(theme.palette.background.paper, 1)})`,
            backdropFilter: 'blur(10px)',
            boxShadow: `0 8px 32px ${alpha(theme.palette.primary.main, 0.1)}`,
            border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
            transition: 'all 0.3s ease',
            '&:hover': {
              boxShadow: `0 12px 40px ${alpha(theme.palette.primary.main, 0.15)}`,
              transform: 'translateY(-5px)'
            }
          }}
        >
          <Typography 
            variant="h4" 
            component="h1" 
            gutterBottom 
            align="center" 
            sx={{
              color: theme.palette.primary.main,
              fontWeight: 'bold',
              mb: 4,
              textShadow: `2px 2px 4px ${alpha(theme.palette.primary.main, 0.2)}`
            }}
          >
            Upload Your Score File
          </Typography>

          {error && (
            <Alert 
              severity="error" 
              sx={{ 
                mb: 2,
                borderRadius: 2,
                animation: `${pulseAnimation} 0.5s ease-in-out`
              }}
            >
              {error}
            </Alert>
          )}

          {success && (
            <Alert 
              severity="success" 
              sx={{ 
                mb: 2,
                borderRadius: 2,
                animation: `${pulseAnimation} 0.5s ease-in-out`
              }}
            >
              {success}
            </Alert>
          )}

          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 3
            }}
          >
            <input
              id="file-input"
              type="file"
              accept=".xlsx"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
            
            <Box
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              sx={{
                width: '100%',
                height: 200,
                border: `2px dashed ${isDragging ? theme.palette.primary.main : alpha(theme.palette.primary.main, 0.3)}`,
                borderRadius: 2,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 2,
                bgcolor: isDragging ? alpha(theme.palette.primary.main, 0.05) : 'transparent',
                transition: 'all 0.3s ease',
                cursor: 'pointer',
                '&:hover': {
                  borderColor: theme.palette.primary.main,
                  bgcolor: alpha(theme.palette.primary.main, 0.05)
                }
              }}
              onClick={() => document.getElementById('file-input').click()}
            >
              <CloudUploadIcon 
                sx={{ 
                  fontSize: 48,
                  color: theme.palette.primary.main,
                  animation: `${floatAnimation} 3s ease-in-out infinite`
                }} 
              />
              <Typography variant="h6" color="textSecondary" align="center">
                Drag and drop your file here
              </Typography>
              <Typography variant="body2" color="textSecondary" align="center">
                or click to browse
              </Typography>
              <Typography variant="caption" color="textSecondary" align="center">
                (Only .xlsx files up to 20MB)
              </Typography>
            </Box>

            {selectedFile && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                style={{ width: '100%' }}
              >
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    gap: 2,
                    p: 2,
                    borderRadius: 2,
                    bgcolor: alpha(theme.palette.primary.main, 0.05),
                    border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      bgcolor: alpha(theme.palette.primary.main, 0.1),
                      transform: 'translateX(8px)'
                    }
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <InsertDriveFileIcon 
                      sx={{ 
                        color: theme.palette.primary.main,
                        fontSize: 32
                      }} 
                    />
                    <Typography variant="body1" color="textSecondary">
                      {selectedFile.name}
                    </Typography>
                  </Box>
                  <IconButton 
                    onClick={removeFile}
                    sx={{
                      color: theme.palette.error.main,
                      '&:hover': {
                        bgcolor: alpha(theme.palette.error.main, 0.1)
                      }
                    }}
                  >
                    <CloseIcon />
                  </IconButton>
                </Box>
              </motion.div>
            )}

            <Button
              variant="contained"
              onClick={handleUpload}
              disabled={!selectedFile || isUploading}
              startIcon={isUploading ? null : <CloudUploadIcon />}
              sx={{
                px: 6,
                py: 2,
                borderRadius: 2,
                background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.primary.dark})`,
                '&:hover': {
                  background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.primary.main})`
                },
                '&:disabled': {
                  background: alpha(theme.palette.primary.main, 0.5)
                }
              }}
            >
              {isUploading ? 'Uploading...' : 'Upload File'}
            </Button>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default FileUpload; 