import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Button,
  useTheme,
  alpha,
  keyframes
} from '@mui/material';
import { motion } from 'framer-motion';

// Animation keyframes
const float = keyframes`
  0% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
  100% { transform: translateY(0px); }
`;

const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const LandingPage = () => {
  const theme = useTheme();
  const navigate = useNavigate();

  const handleStartSurvey = () => {
    navigate('/survey');
  };

  const handleChatWithMe = () => {
    window.open('http://192.168.2.114:4000/', '_blank', 'noopener,noreferrer');
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)}, ${alpha(theme.palette.primary.dark, 0.2)})`,
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Logo */}
      <Box
        component={motion.div}
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8 }}
        sx={{
          position: 'absolute',
          top: 40,
          left: 40,
          zIndex: 1
        }}
      >
        <Typography
          variant="h4"
          sx={{
            fontWeight: 'bold',
            color: theme.palette.primary.main,
            textShadow: `2px 2px 4px ${alpha(theme.palette.primary.main, 0.3)}`,
            fontFamily: 'Arial, sans-serif'
          }}
        >
          HUMG
        </Typography>
      </Box>

      {/* Main Content */}
      <Container maxWidth="lg">
        <Box
          sx={{
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
            py: 8
          }}
        >
          {/* Animated Title */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <Typography
              variant="h2"
              component="h1"
              sx={{
                fontWeight: 'bold',
                mb: 3,
                background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.primary.dark})`,
                backgroundClip: 'text',
                textFillColor: 'transparent',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                animation: `${float} 6s ease-in-out infinite`
              }}
            >
              Hệ thống đánh giá và phân tích kỹ năng học tập
            </Typography>
          </motion.div>

          {/* Description */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <Typography
              variant="h5"
              sx={{
                mb: 6,
                color: theme.palette.text.secondary,
                maxWidth: '800px',
                mx: 'auto',
                animation: `${fadeIn} 1s ease-in`
              }}
            >
              Tham gia khảo sát để giúp chúng tôi hiểu rõ hơn về các yếu tố ảnh hưởng đến quá trình học tập của sinh viên
            </Typography>
          </motion.div>

          {/* Button Container */}
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2, alignItems: 'center' }}>
            {/* Start Survey Button */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.6 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Button
                variant="contained"
                size="large"
                onClick={handleStartSurvey}
                sx={{
                  px: 6,
                  py: 2,
                  fontSize: '1.2rem',
                  borderRadius: '50px',
                  background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.primary.dark})`,
                  boxShadow: `0 8px 16px ${alpha(theme.palette.primary.main, 0.3)}`,
                  '&:hover': {
                    background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.primary.main})`,
                    boxShadow: `0 12px 20px ${alpha(theme.palette.primary.main, 0.4)}`
                  }
                }}
              >
                Bắt đầu khảo sát
              </Button>
            </motion.div>

            {/* Chat with me Button */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.7 }} // Slightly later delay
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Button
                variant="outlined"
                size="large"
                onClick={handleChatWithMe}
                sx={{
                  px: 6,
                  py: 2,
                  fontSize: '1.2rem',
                  borderRadius: '50px',
                  borderColor: theme.palette.secondary.main,
                  color: theme.palette.secondary.main,
                  borderWidth: 2,
                  '&:hover': {
                    backgroundColor: alpha(theme.palette.secondary.main, 0.1),
                    borderColor: theme.palette.secondary.dark,
                    borderWidth: 2,
                  }
                }}
              >
                Chat with me
              </Button>
            </motion.div>
          </Box>

          {/* Decorative Elements */}
          <Box
            sx={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: '100%',
              height: '100%',
              zIndex: -1,
              opacity: 0.1,
              background: `radial-gradient(circle at center, ${theme.palette.primary.main} 0%, transparent 70%)`
            }}
          />
        </Box>
      </Container>
    </Box>
  );
};

export default LandingPage; 