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
  ListItemText,
  Grid
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import SchoolIcon from '@mui/icons-material/School';
import WorkIcon from '@mui/icons-material/Work';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import AssessmentIcon from '@mui/icons-material/Assessment';
import PollIcon from '@mui/icons-material/Poll';
import BarChartIcon from '@mui/icons-material/BarChart';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import axios from 'axios';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';

// Chart.js imports
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  PointElement,
  LineElement,
  ArcElement
} from 'chart.js';
import { Radar, Pie, Line } from 'react-chartjs-2';
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  PointElement,
  LineElement,
  ArcElement,
  ChartDataLabels
);

// Animation keyframes
const gradientAnimation = keyframes`
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
`;

const TypingIndicatorDots = keyframes`
  0%, 80%, 100% { opacity: 0; transform: scale(0.5); }
  40% { opacity: 1; transform: scale(1); }
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
  const [isLlmTyping, setIsLlmTyping] = useState(false);
  const [analysisComplete, setAnalysisComplete] = useState(false);
  const chatBoxRef = useRef(null);

  // State for chart data
  const [skillsChartData, setSkillsChartData] = useState(null);
  const [gradesChartData, setGradesChartData] = useState(null);
  const [gpaTrendChartData, setGpaTrendChartData] = useState(null);
  const [chartError, setChartError] = useState('');

  // Refs for analysis stage content areas
  const stage1Ref = useRef(null);
  const stage2Ref = useRef(null);
  const stage3Ref = useRef(null);
  const activeStageRef = useRef(null); // To know which stage is currently being updated

  const handleLogoClick = () => {
    navigate('/');
  };

  // Fetch data for charts
  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const khaosatRes = await axios.get('http://localhost:5000/api/get-khaosat-summary');
        const diemRes = await axios.get('http://localhost:5000/api/get-data');

        // Process skills data (Radar Chart)
        const skillsData = khaosatRes.data;
        const predefinedSkillLabels = [
          "Thái độ học tập",
          "Sử dụng mạng xã hội",
          "Gia đình – Xã hội",
          "Bạn bè",
          "Môi trường học tập",
          "Kỹ năng Quản lý thời gian",
          "Kỹ năng tự học",
          "Kỹ năng làm việc nhóm",
          "Tư duy phản biện",
          "Tiếp thu & xử lý kiến thức"
        ];
        const skillKeys = [
            "Thai_do_hoc_tap",
            "Su_dung_mang_xa_hoi",
            "Gia_dinh_Xa_hoi",
            "Ban_be",
            "Moi_truong_hoc_tap",
            "Quan_ly_thoi_gian",
            "Tu_hoc",
            "Hop_tac_nhom",
            "Tu_duy_phan_bien",
            "Tiep_thu_xu_ly_kien_thuc"
        ];

        const skillPercentages = skillKeys.map(key => skillsData[key]?.phan_tram_diem || 0);
        
        if (skillPercentages.length > 0) {
          setSkillsChartData({
            labels: predefinedSkillLabels,
            datasets: [
              {
                label: 'Tỷ lệ % Kỹ năng',
                data: skillPercentages,
                backgroundColor: alpha(theme.palette.primary.main, 0.2),
                borderColor: theme.palette.primary.main,
                borderWidth: 2,
                pointBackgroundColor: theme.palette.primary.main,
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: theme.palette.primary.main
              },
            ],
          });
        }

        // Process grades data (Pie Chart)
        const diemData = diemRes.data?.data;
        const semesters = diemData?.ds_diem_hocky || [];
        const gradeCounts = {};
        semesters.forEach(semester => {
          semester.ds_diem_mon_hoc?.forEach(course => {
            const grade = course.diem_tk_chu;
            if (grade && grade.trim() !== '') {
              gradeCounts[grade] = (gradeCounts[grade] || 0) + 1;
            }
          });
        });

        if (Object.keys(gradeCounts).length > 0) {
          const gradeLabels = Object.keys(gradeCounts);
          const gradeValues = Object.values(gradeCounts);
          setGradesChartData({
            labels: gradeLabels,
            datasets: [
              {
                label: 'Số lượng môn',
                data: gradeValues,
                backgroundColor: [
                  '#FF6384', // Red
                  '#36A2EB', // Blue
                  '#FFCE56', // Yellow
                  '#4BC0C0', // Teal
                  '#9966FF', // Purple
                  '#FF9F40', // Orange
                  '#8D6E63', // Brown
                  '#EC407A', // Pink
                  '#78909C', // Blue Grey
                  '#66BB6A', // Light Green
                  '#26A69A', // Dark Teal
                  '#AB47BC'  // Light Purple
                  // Add more distinct colors if you expect more than 12 unique grade types
                ],
                borderColor: theme.palette.background.paper,
                borderWidth: 2,
              },
            ],
          });
        }

        // Process GPA Trend data (Line Chart)
        if (semesters.length > 0) {
          // Sort semesters from oldest to newest for the chart
          const sortedSemesters = [...semesters].reverse(); 
          const gpaLabels = sortedSemesters.map(s => s.ten_hoc_ky || 'N/A');
          const gpaValues = sortedSemesters.map(s => parseFloat(s.dtb_tich_luy_he_4) || null); // Ensure numeric, null for missing
          
          setGpaTrendChartData({
            labels: gpaLabels,
            datasets: [
              {
                label: 'Điểm TB Tích Lũy (Hệ 4)',
                data: gpaValues,
                borderColor: theme.palette.secondary.main,
                backgroundColor: alpha(theme.palette.secondary.main, 0.1),
                fill: true,
                tension: 0.1, // For a slightly curved line
                pointRadius: 5,
                pointBackgroundColor: theme.palette.secondary.main,
                pointHoverRadius: 7,
              },
            ],
          });
        }

      } catch (err) {
        console.error("Error fetching chart data:", err);
        setChartError('Không thể tải dữ liệu cho biểu đồ.');
      }
    };
    fetchChartData();
  }, [theme.palette]);

  const handleStartAnalysis = () => {
    setIsLoading(true);
    setError('');
    setAnalysisComplete(false);
    const initialStages = {
      stage1_khaosat: 'Đang xử lý giai đoạn này...',
      stage2_diem: 'Đang xử lý giai đoạn này...',
      stage3_tonghop: 'Đang xử lý giai đoạn này...'
    };
    setAnalysisStages(initialStages);
    setChatHistory([]);

    const eventSource = new EventSource('http://localhost:5000/api/start-llm-analysis', { method: 'POST' });
    let currentStageKey = null; // Will be 'stage1_khaosat', 'stage2_diem', or 'stage3_tonghop'
    let stageBuffers = { stage1_khaosat: '', stage2_diem: '', stage3_tonghop: '' };

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.error) {
          setError(data.error);
          setAnalysisStages(prev => ({
            ...prev,
            [data.stage || currentStageKey]: `<p style='color:red;'>Lỗi: ${data.error}</p>`
          }));
          setIsLoading(false);
          eventSource.close();
          return;
        }

        if (data.stage) {
          currentStageKey = data.stage; // e.g., "stage1_khaosat"
          if (currentStageKey === 'stage1_khaosat') activeStageRef.current = stage1Ref.current;
          else if (currentStageKey === 'stage2_diem') activeStageRef.current = stage2Ref.current;
          else if (currentStageKey === 'stage3_tonghop') activeStageRef.current = stage3Ref.current;
          
          if (data.token) {
            stageBuffers[data.stage] += data.token;
            setAnalysisStages(prev => ({ ...prev, [data.stage]: stageBuffers[data.stage] }));
          }
        }

        if (data.status === 'all_done' || data.status?.startsWith('error_stage')) {
          setIsLoading(false);
          setAnalysisComplete(true);
          activeStageRef.current = null; // Reset active stage ref
          eventSource.close();
        }
      } catch (e) {
        console.error("Error parsing SSE data:", e);
        setError("Lỗi xử lý dữ liệu từ server.");
        setIsLoading(false);
        activeStageRef.current = null;
        eventSource.close();
      }
    };

    eventSource.onerror = (err) => {
      console.error("EventSource failed:", err);
      setError("Lỗi kết nối đến server phân tích.");
      setIsLoading(false);
      activeStageRef.current = null;
      eventSource.close();
    };
  };

  const handleSendChat = async () => {
    if (!chatInput.trim() || isChatting || isLlmTyping) return;

    const userMessage = { role: 'user', content: chatInput };
    setChatHistory(prev => [...prev, userMessage]);
    setChatInput('');
    setIsChatting(true);
    setIsLlmTyping(true);

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
                    setChatHistory(prev => [...prev, { role: 'assistant', content: assistantMessageContent }]);
                    firstChunk = false;
                  } else {
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

      const readStream = async () => {
        const { done, value } = await reader.read();
        if (done) {
          setIsChatting(false); 
          setIsLlmTyping(false);
          return;
        }
        const chunk = decoder.decode(value, { stream: true });
        processChunk(chunk);
        readStream(); 
      };

      readStream(); 

    } catch (error) {
      console.error('Chat error:', error);
      setChatHistory(prev => [...prev, { role: 'assistant', content: 'Xin lỗi, đã có lỗi xảy ra.' }]);
      setIsChatting(false); 
      setIsLlmTyping(false);
    }
  };

  // useEffect for chatBox scroll
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chatHistory]);

  // useEffect for auto-scrolling analysis content
  useEffect(() => {
    if (isLoading && activeStageRef.current) {
      const contentElement = activeStageRef.current; // This is the Paper element
      const rect = contentElement.getBoundingClientRect();
      const viewportHeight = window.innerHeight;

      // If the bottom of the content is more than 70% down the viewport (i.e., close to bottom)
      if (rect.bottom > viewportHeight * 0.7) {
        // Calculate how much to scroll to bring the bottom of the content to roughly vertical center
        const scrollAmount = rect.bottom - viewportHeight / 2;
        // Only scroll if there's a significant amount to scroll to avoid jitter
        if (scrollAmount > 0) { 
          window.scrollBy({
            top: scrollAmount,
            behavior: 'smooth'
          });
        }
      }
    }
  }, [analysisStages, isLoading]); // Rerun when analysisStages or isLoading changes

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

  const radarOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: { color: theme.palette.text.primary, font: { size: 14 } }
      },
      title: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.formattedValue !== null) {
              label += context.formattedValue + '%';
            }
            return label;
          }
        }
      }
    },
    scales: {
      r: {
        angleLines: { color: alpha(theme.palette.text.secondary, 0.5) },
        grid: { color: alpha(theme.palette.text.secondary, 0.5) },
        pointLabels: { 
          font: { size: 12 }, 
          color: theme.palette.text.primary 
        },
        min: 0,
        max: 100,
        ticks: {
          stepSize: 20,
          backdropColor: 'transparent',
          color: theme.palette.text.secondary
        }
      }
    }
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
        labels: { color: theme.palette.text.primary, font: { size: 14 }, boxWidth: 20 }
      },
      title: {
        display: false,
      },
      tooltip: {
        enabled: true, 
        callbacks: {
          label: function(context) {
            let label = context.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed !== null) {
              label += context.parsed + (context.parsed === 1 ? ' môn' : ' môn'); 
            }
            return label;
          }
        }
      },
      datalabels: { 
        display: true,
        color: theme.palette.common.white,
        anchor: 'center', 
        align: 'center', 
        formatter: (value, context) => {
          return `${value} môn`;
        },
        font: {
          weight: 'bold',
          size: 12,
        },
        textStrokeColor: alpha(theme.palette.common.black, 0.8),
        textStrokeWidth: 2,
        borderRadius: 4,
        backgroundColor: alpha(theme.palette.common.black, 0.6),
        padding: { top: 5, bottom: 4, left: 7, right: 7 }
      }
    }
  };

  const lineChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: { color: theme.palette.text.primary, font: { size: 14 } }
      },
      title: {
        display: false, // Or set a title: text: 'Xu Hướng Điểm GPA Tích Lũy'
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += context.parsed.y.toFixed(2);
            }
            return label;
          }
        }
      },
      datalabels: { // Disable datalabels for line chart for cleaner look, rely on tooltips and points
        display: false,
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Học Kỳ',
          color: theme.palette.text.secondary,
          font: { size: 12, weight: 'bold' }
        },
        ticks: { color: theme.palette.text.secondary, font: {size: 10} }
      },
      y: {
        title: {
          display: true,
          text: 'Điểm GPA (Hệ 4)',
          color: theme.palette.text.secondary,
          font: { size: 12, weight: 'bold' }
        },
        ticks: { color: theme.palette.text.secondary },
        beginAtZero: false, // Start y-axis near the lowest data point for better visualization of change
        // suggestedMin: 1, // Or set a specific min if GPA scale is known
        // suggestedMax: 4   // Or set a specific max
      }
    }
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

          {/* Charts Section */}
          <Box sx={{ mb: 4 }}>
            <Accordion defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="h5" sx={{ color: theme.palette.primary.dark, display: 'flex', alignItems: 'center' }}>
                        <AssessmentIcon sx={{ mr: 1.5, color: theme.palette.secondary.main }}/> Tổng Quan Trực Quan
                    </Typography>
                </AccordionSummary>
                <AccordionDetails>
                    {chartError && <Alert severity="error" sx={{ mb: 2 }}>{chartError}</Alert>}
                    <Grid container spacing={4} alignItems="stretch">
                        <Grid item xs={12} sm={6}> {/* Skills chart: half width on small screens and up */}
                            <Paper elevation={2} sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}> 
                                <Typography variant="h6" gutterBottom align="center" sx={{ display: 'flex', alignItems: 'center'}}>
                                    <PollIcon sx={{mr:1, color: theme.palette.info.main}}/> Biểu Đồ Kỹ Năng
                                </Typography>
                                {skillsChartData ? (
                                    <Box sx={{ flexGrow: 1, width: '100%', height: 350 }}>
                                      <Radar data={skillsChartData} options={radarOptions} />
                                    </Box>
                                ) : <CircularProgress />}
                                <Typography variant="caption" sx={{ mt: 1, textAlign: 'center'}}>
                                    Ghi chú: Biểu đồ thể hiện tỷ lệ % các kỹ năng dựa trên khảo sát.
                                </Typography>
                            </Paper>
                        </Grid>
                        <Grid item xs={12} sm={6}> {/* Grades chart: half width on small screens and up */}
                            <Paper elevation={2} sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}> 
                                <Typography variant="h6" gutterBottom align="center" sx={{ display: 'flex', alignItems: 'center'}}>
                                   <BarChartIcon sx={{mr:1, color: theme.palette.success.main}}/> Phân Bổ Điểm Chữ
                                </Typography>
                                {gradesChartData ? (
                                    <Box sx={{ flexGrow: 1, width: '100%', height: 350 }}>
                                      <Pie data={gradesChartData} options={pieOptions} />
                                    </Box>
                                ) : <CircularProgress />}
                                <Typography variant="caption" sx={{ mt: 1, textAlign: 'center'}}>
                                    Ghi chú: Biểu đồ thể hiện số lượng môn học theo từng loại điểm chữ.
                                </Typography>
                            </Paper>
                        </Grid>
                        <Grid item xs={12}> {/* GPA Trend chart: full width on all screens, will naturally go to next line */}
                            <Paper elevation={2} sx={{ p: 2, mt: 4, height: 400, display: 'flex', flexDirection: 'column', alignItems: 'center' }}> {/* Added mt for spacing, adjusted height */}
                                <Typography variant="h6" gutterBottom align="center" sx={{ display: 'flex', alignItems: 'center'}}>
                                   <AssessmentIcon sx={{mr:1, color: theme.palette.secondary.dark}}/> Xu Hướng GPA Tích Lũy
                                </Typography>
                                {gpaTrendChartData ? (
                                    <Box sx={{ flexGrow: 1, width: '100%', height: '100%' }}>
                                      <Line data={gpaTrendChartData} options={lineChartOptions} />
                                    </Box>
                                ) : <CircularProgress />}
                                <Typography variant="caption" sx={{ mt: 1, textAlign: 'center'}}>
                                    Ghi chú: Biểu đồ thể hiện xu hướng điểm GPA tích lũy (hệ 4) qua các học kỳ (sắp xếp từ cũ nhất đến mới nhất).
                                </Typography>
                            </Paper>
                        </Grid>
                    </Grid>
                </AccordionDetails>
            </Accordion>
          </Box>

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
                <Paper ref={stage1Ref} elevation={0} sx={{ p: 2, bgcolor: alpha(theme.palette.primary.main, 0.02), borderRadius: 1 }}>
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
                <Paper ref={stage2Ref} elevation={0} sx={{ p: 2, bgcolor: alpha(theme.palette.primary.main, 0.02), borderRadius: 1 }}>
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
                <Paper ref={stage3Ref} elevation={0} sx={{ p: 2, bgcolor: alpha(theme.palette.primary.main, 0.02), borderRadius: 1 }}>
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
                      boxShadow: 1,
                      color: msg.role === 'user' ? theme.palette.primary.contrastText : theme.palette.text.primary,
                    }}
                  >
                    <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
                      {msg.content}
                    </ReactMarkdown>
                  </Box>
                ))}
                {isLlmTyping && (
                  <ListItem sx={{ justifyContent: 'flex-start', px: 1.5, py: 1 }}>
                    <ListItemIcon sx={{minWidth: 40}}>
                        <MoreHorizIcon 
                            sx={{
                                color: theme.palette.text.secondary,
                                animation: `${TypingIndicatorDots} 1.4s infinite ease-in-out both`,
                                '& > circle:nth-of-type(1)': {
                                    animationDelay: '-0.32s'
                                },
                                '& > circle:nth-of-type(2)': {
                                    animationDelay: '-0.16s'
                                }
                            }}
                        />
                    </ListItemIcon>
                    <ListItemText 
                        primary="Chuyên gia đang nhập..."
                        primaryTypographyProps={{ variant: 'body2', color: 'textSecondary', fontStyle: 'italic' }}
                    />
                  </ListItem>
                )}
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