import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Alert,
  CircularProgress,
  TextField,
  IconButton,
  useTheme,
  alpha,
  keyframes,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import SchoolIcon from '@mui/icons-material/School';
import WorkIcon from '@mui/icons-material/Work';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';

// Animation keyframes
const gradientAnimation = keyframes`
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
`;

const AnalysisPage = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [analysisStages, setAnalysisStages] = useState({
    stage1_khaosat: 'Chưa có dữ liệu...',
    stage2_diem: 'Chưa có dữ liệu...',
    stage3_tonghop: 'Chưa có dữ liệu...'
  });
  const [error, setError] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [isChatting, setIsChatting] = useState(false);
  const [analysisComplete, setAnalysisComplete] = useState(false);
  const chatBoxRef = useRef(null);

  const handleLogoClick = () => {
    navigate('/');
  };

  const handleStartAnalysis = () => {
    setIsLoading(true);
    setError('');
    setAnalysisComplete(false);
    setAnalysisStages({
      stage1_khaosat: 'Đang xử lý giai đoạn này...',
      stage2_diem: 'Đang xử lý giai đoạn này...',
      stage3_tonghop: 'Đang xử lý giai đoạn này...'
    });
    setChatHistory([]); // Clear previous chat

    const eventSource = new EventSource('http://localhost:5000/api/start-llm-analysis', { method: 'POST' });
    let currentStage = null;
    let stageBuffers = { stage1_khaosat: '', stage2_diem: '', stage3_tonghop: '' };

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.error) {
          setError(data.error);
          setAnalysisStages(prev => ({
            ...prev,
            [data.stage || currentStage]: `<p style='color:red;'>Lỗi: ${data.error}</p>`
          }));
          setIsLoading(false);
          eventSource.close();
          return;
        }

        if (data.stage) {
          currentStage = data.stage;
          if (data.token) {
            stageBuffers[data.stage] += data.token;
            setAnalysisStages(prev => ({ ...prev, [data.stage]: stageBuffers[data.stage] }));
          }
        }

        if (data.status === 'all_done' || data.status?.startsWith('error_stage')) {
          setIsLoading(false);
          setAnalysisComplete(true);
          eventSource.close();
        }
      } catch (e) {
        console.error("Error parsing SSE data:", e);
        setError("Lỗi xử lý dữ liệu từ server.");
        setIsLoading(false);
        eventSource.close();
      }
    };

    eventSource.onerror = (err) => {
      console.error("EventSource failed:", err);
      setError("Lỗi kết nối đến server phân tích.");
      setIsLoading(false);
      setAnalysisStages({
        stage1_khaosat: 'Lỗi kết nối.',
        stage2_diem: 'Lỗi kết nối.',
        stage3_tonghop: 'Lỗi kết nối.'
      });
      eventSource.close();
    };
  };

  const handleSendChat = async () => {
    if (!chatInput.trim() || isChatting) return;

    const userMessage = { role: 'user', content: chatInput };
    setChatHistory(prev => [...prev, userMessage]);
    setChatInput('');
    setIsChatting(true);

    try {
      const response = await fetch('http://localhost:5000/api/llm-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage.content })
      });

      if (!response.ok || !response.body) {
        throw new Error('Network response was not ok or no body');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantMessageContent = '';
      let firstChunk = true;

      // Define the function to process stream chunks outside the loop
      const processChunk = (chunk) => {
        const lines = chunk.split('\n\n');
        lines.forEach(line => {
          if (line.startsWith('data: ')) {
            const jsonDataString = line.substring(6).trim();
            if (jsonDataString) {
              try {
                const data = JSON.parse(jsonDataString);
                if (data.token) {
                  assistantMessageContent += data.token;
                  if (firstChunk) {
                    // Add new assistant message
                    setChatHistory(prev => [...prev, { role: 'assistant', content: assistantMessageContent }]);
                    firstChunk = false;
                  } else {
                    // Update the last assistant message
                    setChatHistory(prev => prev.map((msg, index) => 
                      index === prev.length - 1 ? { ...msg, content: assistantMessageContent } : msg
                    ));
                  }
                }
              } catch (e) {
                console.error('Error parsing chat JSON:', e);
              }
            }
          }
        });
      };

      // Define the recursive read function
      const readStream = async () => {
        const { done, value } = await reader.read();
        if (done) {
          setIsChatting(false); // Ensure chatting state is reset when stream ends
          return;
        }
        const chunk = decoder.decode(value, { stream: true });
        processChunk(chunk);
        readStream(); // Continue reading
      };

      readStream(); // Start reading the stream

    } catch (error) {
      console.error('Chat error:', error);
      setChatHistory(prev => [...prev, { role: 'assistant', content: 'Xin lỗi, đã có lỗi xảy ra.' }]);
      setIsChatting(false); // Reset chatting state on error
    }
  };

  useEffect(() => {
    // Scroll chat box to bottom
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const renderMarkdownContent = (content, stageKey) => {
    // Helper to get appropriate icon based on heading text or list item content
    const getIconForText = (text) => {
      const lowerText = text.toLowerCase();
      if (lowerText.includes('điểm mạnh') || lowerText.includes('strengths') || lowerText.includes('ưu điểm')) return <CheckCircleOutlineIcon sx={{ color: theme.palette.success.main, mr: 1 }} />;
      if (lowerText.includes('điểm yếu') || lowerText.includes('weaknesses') || lowerText.includes('cần cải thiện')) return <HighlightOffIcon sx={{ color: theme.palette.error.main, mr: 1 }} />;
      if (lowerText.includes('kỹ năng') || lowerText.includes('skills')) return <SchoolIcon sx={{ color: theme.palette.info.main, mr: 1 }} />;
      if (lowerText.includes('khuyến nghị') || lowerText.includes('recommendations') || lowerText.includes('định hướng')) return <WorkIcon sx={{ color: theme.palette.warning.main, mr: 1 }} />;
      if (lowerText.includes('lời khuyên') || lowerText.includes('advice') || lowerText.includes('tips')) return <LightbulbIcon sx={{ color: theme.palette.secondary.main, mr: 1 }} />;
      return null;
    };

    return (
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={{
          h1: ({ node, ...props }) => {
            const icon = getIconForText(node.children[0]?.value || '');
            return <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>{icon}{props.children}</Typography>;
          },
          h2: ({ node, ...props }) => {
            const icon = getIconForText(node.children[0]?.value || '');
            return <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', mt: 3 }}>{icon}{props.children}</Typography>;
          },
          h3: ({ node, ...props }) => {
            const icon = getIconForText(node.children[0]?.value || '');
            return <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>{icon}{props.children}</Typography>;
          },
          p: ({ node, ...props }) => <Typography variant="body1" paragraph {...props} />,
          ul: ({ node, ...props }) => <List dense sx={{ pl: 2 }}>{props.children}</List>,
          li: ({ node, ...props }) => {
            // Attempt to get text from the first child paragraph or direct text
            let textContent = '';
            if (node.children[0]?.type === 'paragraph' && node.children[0]?.children[0]?.type === 'text') {
              textContent = node.children[0].children[0].value;
            } else if (node.children[0]?.type === 'text') {
              textContent = node.children[0].value;
            }
            const icon = getIconForText(textContent);
            return (
              <ListItem sx={{ display: 'flex', alignItems: 'flex-start', py: 0.5 }}>
                {icon && <ListItemIcon sx={{ minWidth: 32, mt: '4px' }}>{icon}</ListItemIcon>}
                <ListItemText primary={<Typography variant="body1" component="span">{props.children}</Typography>} />
              </ListItem>
            );
          },
          blockquote: ({ node, ...props }) => (
            <Box component={Paper} elevation={1} sx={{ 
              borderLeft: `5px solid ${theme.palette.primary.main}`,
              pl: 2, my: 2, py: 1, fontStyle: 'italic', 
              bgcolor: alpha(theme.palette.primary.main, 0.05)
            }} {...props} />
          ),
          code: ({node, inline, className, children, ...props}) => {
            const match = /language-(\w+)/.exec(className || '')
            return !inline && match ? (
              // For code blocks, you might want to use a syntax highlighter later
              <Paper elevation={0} sx={{ p: 1.5, my: 1.5, bgcolor: alpha(theme.palette.grey[500], 0.1), overflowX: 'auto', borderRadius: 1}}>
                <pre style={{margin: 0}}><code className={className} {...props}>{children}</code></pre>
              </Paper>
            ) : (
              <Chip label={children} size="small" sx={{ bgcolor: alpha(theme.palette.secondary.main, 0.1), color: theme.palette.secondary.dark, mx: 0.5 }} />
            )
          },
          table: ({node, ...props}) => <Box component={Paper} elevation={1} sx={{my: 2, p:1, overflowX: 'auto'}}><table style={{width: '100%', borderCollapse: 'collapse'}} {...props} /> </Box>,
          th: ({node, ...props}) => <th style={{border: `1px solid ${theme.palette.divider}`, padding: theme.spacing(1), textAlign: 'left', background: alpha(theme.palette.grey[200], 0.7)}} {...props} />,
          td: ({node, ...props}) => <td style={{border: `1px solid ${theme.palette.divider}`, padding: theme.spacing(1)}} {...props} />,
        }}
      >
        {content}
      </ReactMarkdown>
    );
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: `linear-gradient(-45deg, 
          ${alpha(theme.palette.primary.main, 0.05)}, 
          ${alpha(theme.palette.primary.dark, 0.1)}, 
          ${alpha(theme.palette.primary.main, 0.1)}, 
          ${alpha(theme.palette.primary.dark, 0.05)})`,
        backgroundSize: '400% 400%',
        animation: `${gradientAnimation} 20s ease infinite`,
        position: 'relative',
        overflow: 'hidden',
        py: 4
      }}
    >
      <Box
        onClick={handleLogoClick}
        sx={{
          position: 'absolute',
          top: 40,
          left: 40,
          zIndex: 2,
          cursor: 'pointer',
          transition: 'transform 0.2s ease-in-out',
          '&:hover': {
            transform: 'scale(1.05)'
          }
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

      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1, pt: 12 }}>
        <Paper 
          elevation={3} 
          sx={{ 
            p: 4, 
            borderRadius: 2,
            background: alpha(theme.palette.background.paper, 0.95),
            backdropFilter: 'blur(5px)',
            boxShadow: `0 8px 32px ${alpha(theme.palette.primary.main, 0.1)}`,
            border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`
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
              textShadow: `1px 1px 3px ${alpha(theme.palette.primary.main, 0.2)}`
            }}
          >
            Phân tích Kỹ năng Học tập Sinh viên
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>
          )}

          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 4 }}>
            <Button
              variant="contained"
              onClick={handleStartAnalysis}
              disabled={isLoading}
              startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : null}
              sx={{
                px: 5,
                py: 1.5,
                background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.primary.dark})`,
                '&:hover': { background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.primary.main})` }
              }}
            >
              {isLoading ? 'Đang phân tích...' : 'Bắt đầu Phân tích'}
            </Button>
          </Box>

          {/* Analysis Stages with Accordion */}
          <Box sx={{ mb: 2 }}>
            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h5" sx={{ color: theme.palette.primary.dark, display: 'flex', alignItems: 'center' }}>
                  <SchoolIcon sx={{ mr: 1.5, color: theme.palette.info.main }} /> Phân tích Kỹ năng Học tập
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Paper elevation={0} sx={{ p: 2, bgcolor: alpha(theme.palette.primary.main, 0.02), borderRadius: 1 }}>
                  {renderMarkdownContent(analysisStages.stage1_khaosat, 'stage1_khaosat')}
                </Paper>
              </AccordionDetails>
            </Accordion>
          </Box>

          <Box sx={{ mb: 2 }}>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h5" sx={{ color: theme.palette.primary.dark, display: 'flex', alignItems: 'center' }}>
                  <WorkIcon sx={{ mr: 1.5, color: theme.palette.warning.main }} /> Phân tích Điểm số
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Paper elevation={0} sx={{ p: 2, bgcolor: alpha(theme.palette.primary.main, 0.02), borderRadius: 1 }}>
                  {renderMarkdownContent(analysisStages.stage2_diem, 'stage2_diem')}
                </Paper>
              </AccordionDetails>
            </Accordion>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h5" sx={{ color: theme.palette.primary.dark, display: 'flex', alignItems: 'center' }}>
                  <LightbulbIcon sx={{ mr: 1.5, color: theme.palette.secondary.main }} /> Tư vấn Tổng hợp
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Paper elevation={0} sx={{ p: 2, bgcolor: alpha(theme.palette.primary.main, 0.02), borderRadius: 1 }}>
                  {renderMarkdownContent(analysisStages.stage3_tonghop, 'stage3_tonghop')}
                </Paper>
              </AccordionDetails>
            </Accordion>
          </Box>
          
          {/* Chat Interface */}
          {analysisComplete && (
            <Box sx={{ mt: 5 }}>
              <Typography variant="h5" gutterBottom sx={{ color: theme.palette.primary.dark }}>Hỏi thêm Chuyên gia Tư vấn</Typography>
              <Paper ref={chatBoxRef} elevation={1} sx={{ height: 400, overflowY: 'auto', p: 2, mb: 2, bgcolor: alpha(theme.palette.grey[100], 0.7), borderRadius: 2 }}>
                {chatHistory.map((msg, index) => (
                  <Box 
                    key={index} 
                    sx={{ 
                      mb: 1.5, 
                      p: 1.5, 
                      borderRadius: 2, 
                      maxWidth: '80%', 
                      bgcolor: msg.role === 'user' ? theme.palette.primary.light : theme.palette.background.paper,
                      ml: msg.role === 'user' ? 'auto' : 'none',
                      mr: msg.role === 'assistant' ? 'auto' : 'none',
                      boxShadow: 1
                    }}
                  >
                    <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
                      {msg.content}
                    </ReactMarkdown>
                  </Box>
                ))}
              </Paper>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField
                  fullWidth
                  variant="outlined"
                  placeholder="Nhập câu hỏi của bạn..."
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendChat()}
                  disabled={isChatting}
                  sx={{ bgcolor: theme.palette.background.paper, borderRadius: 1 }}
                />
                <IconButton 
                  color="primary" 
                  onClick={handleSendChat} 
                  disabled={isChatting || !chatInput.trim()}
                  sx={{ bgcolor: theme.palette.primary.main, color: 'white', '&:hover': { bgcolor: theme.palette.primary.dark } }}
                >
                  <SendIcon />
                </IconButton>
              </Box>
            </Box>
          )}
        </Paper>
      </Container>
    </Box>
  );
};

export default AnalysisPage; 