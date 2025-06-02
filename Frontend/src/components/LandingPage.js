import React, { useEffect } from 'react';
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
import { motion, useAnimation } from 'framer-motion';

// Import logos
import humgLogo from '../image/HUMG_Logo_transparency.png';
import cnttLogo from '../image/Logo_CNTT1_High res.png';

// Enhanced Animation keyframes
const float = keyframes`
  0% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(1deg); }
  100% { transform: translateY(0px) rotate(0deg); }
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

const gradientFlow = keyframes`
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
`;

const LandingPage = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const controls = useAnimation();

  useEffect(() => {
    controls.start({
      opacity: 1,
      y: 0,
      transition: { duration: 0.8 }
    });
  }, [controls]);

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
        position: 'relative',
        overflow: 'hidden',
        background: `linear-gradient(135deg, 
          ${alpha(theme.palette.primary.main, 0.05)}, 
          ${alpha(theme.palette.primary.dark, 0.1)})`,
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `radial-gradient(circle at 50% 50%, 
            ${alpha(theme.palette.primary.main, 0.1)} 0%, 
            transparent 50%)`,
          animation: `${pulse} 8s ease-in-out infinite`,
          zIndex: 0
        }
      }}
    >
      {/* Animated Background Particles */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          overflow: 'hidden',
          zIndex: 0,
          '&::before': {
            content: '""',
            position: 'absolute',
            width: '200%',
            height: '200%',
            background: `radial-gradient(circle at center, 
              ${alpha(theme.palette.primary.main, 0.1)} 0%, 
              transparent 50%)`,
            animation: `${gradientFlow} 15s ease infinite`,
            backgroundSize: '200% 200%'
          }
        }}
      />

      {/* HUMG Logo (Top-Left) */}
      <motion.div
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8, delay: 0.1 }}
        style={{
          position: 'absolute',
          top: '2rem',
          left: '2rem',
          zIndex: 2
        }}
      >
        <img 
          src={humgLogo} 
          alt="HUMG Logo" 
          style={{ 
            height: 'auto',
            width: 'auto',
            maxHeight: '80px',
            maxWidth: '200px',
            filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.1))'
          }} 
        />
      </motion.div>

      {/* CNTT Logo (Top-Right) */}
      <motion.div
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        style={{
          position: 'absolute',
          top: '2rem',
          right: '2rem',
          zIndex: 2
        }}
      >
        <img 
          src={cnttLogo} 
          alt="CNTT Logo" 
          style={{ 
            height: 'auto',
            width: 'auto',
            maxHeight: '70px',
            maxWidth: '170px',
            filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.1))'
          }} 
        />
      </motion.div>

      {/* Main Content */}
      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
        <Box
          sx={{
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
            pt: { xs: 16, sm: 14, md: 12 },
            pb: 8
          }}
        >
          {/* Conference Title */}
          <motion.div
            initial={{ opacity: 0, y: -30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.3 }}
          >
            <Typography
              variant="h4"
              component="h2"
              sx={{
                fontWeight: 500,
                mb: 2,
                color: theme.palette.text.secondary,
                letterSpacing: '0.5px',
                textShadow: '0 2px 4px rgba(0,0,0,0.1)'
              }}
            >
              Hội nghị Nghiên cứu Khoa học sinh viên lần thứ 38
            </Typography>
          </motion.div>

          {/* Main Title */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
          >
            <Typography
              variant="h2"
              component="h1"
              sx={{
                fontWeight: 'bold',
                mb: 4,
                background: `linear-gradient(45deg, 
                  ${theme.palette.primary.main}, 
                  ${theme.palette.primary.dark})`,
                backgroundClip: 'text',
                textFillColor: 'transparent',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                animation: `${float} 6s ease-in-out infinite`,
                textShadow: '0 4px 8px rgba(0,0,0,0.1)',
                fontSize: { xs: '2.5rem', sm: '3rem', md: '3.5rem' }
              }}
            >
              Khảo sát yếu tố ảnh hưởng đến học tập
            </Typography>
          </motion.div>

          {/* Description */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.7 }}
          >
            <Typography
              variant="h5"
              sx={{
                mb: 8,
                color: theme.palette.text.secondary,
                maxWidth: '800px',
                mx: 'auto',
                lineHeight: 1.6,
                fontWeight: 400
              }}
            >
              Tham gia khảo sát để giúp chúng tôi hiểu rõ hơn về các yếu tố ảnh hưởng đến quá trình học tập của sinh viên
            </Typography>
          </motion.div>

          {/* Button Container */}
          <Box 
            sx={{ 
              display: 'flex', 
              flexDirection: { xs: 'column', sm: 'row' }, 
              gap: 3,
              alignItems: 'center',
              mt: 2
            }}
          >
            {/* Start Survey Button */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.9 }}
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
                  background: `linear-gradient(45deg, 
                    ${theme.palette.primary.main}, 
                    ${theme.palette.primary.dark})`,
                  boxShadow: `0 8px 16px ${alpha(theme.palette.primary.main, 0.3)}`,
                  '&:hover': {
                    background: `linear-gradient(45deg, 
                      ${theme.palette.primary.dark}, 
                      ${theme.palette.primary.main})`,
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
              transition={{ duration: 0.5, delay: 1.1 }}
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
                  backdropFilter: 'blur(8px)',
                  backgroundColor: alpha(theme.palette.background.paper, 0.8),
                  '&:hover': {
                    backgroundColor: alpha(theme.palette.secondary.main, 0.1),
                    borderColor: theme.palette.secondary.dark,
                    borderWidth: 2,
                    boxShadow: `0 8px 16px ${alpha(theme.palette.secondary.main, 0.2)}`
                  }
                }}
              >
                Chat with me
              </Button>
            </motion.div>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default LandingPage; 