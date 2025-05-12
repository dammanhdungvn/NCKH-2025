import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  TextField,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Button,
  Box,
  Alert,
  LinearProgress,
  Stepper,
  Step,
  StepLabel,
  Card,
  CardContent,
  Fade,
  Zoom,
  useTheme,
  alpha,
  keyframes
} from '@mui/material';
import { motion } from 'framer-motion';
import axios from 'axios';

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

const sections = [
  { key: 'A', label: 'Thông tin chung' },
  { key: 'I', label: 'Thái độ học tập' },
  { key: 'II', label: 'Sử dụng mạng xã hội' },
  { key: 'III', label: 'Gia đình – Xã hội' },
  { key: 'IV', label: 'Bạn bè' },
  { key: 'V', label: 'Môi trường học tập' },
  { key: 'VI', label: 'Quản lý thời gian' },
  { key: 'VII', label: 'Tự học' },
  { key: 'VIII', label: 'Hợp tác nhóm' },
  { key: 'IX', label: 'Tư duy phản biện' },
  { key: 'X', label: 'Tiếp thu & xử lý kiến thức' }
];

const sectionQuestions = {
  'I': [
    'Tôi nghiêm túc đặt và theo đuổi mục tiêu học tập rõ ràng mỗi học kỳ.',
    'Tôi chịu trách nhiệm với kết quả học tập và luôn cố gắng cải thiện.',
    'Tôi kiên trì học ngay cả khi gặp khó khăn hoặc thất bại.',
    'Tôi xem việc học tại HUMG là ưu tiên hàng đầu so với hoạt động giải trí.',
    'Tôi thường tự đánh giá và điều chỉnh thái độ học tập khi thấy hiệu quả chưa cao.'
  ],
  'II': [
    'Việc sử dụng mạng xã hội thường làm tôi phân tâm và trì hoãn học tập.',
    'Tôi tận dụng YouTube, blog, fanpage học thuật để tìm tài liệu và video hướng dẫn.',
    'Tôi thường dùng nhóm Facebook/Google Classroom hoặc chat Zalo lớp để trao đổi bài tập.',
    'Tôi kiểm soát tốt thời gian online, không để ảnh hưởng đến việc ôn bài và nộp bài đúng hạn.',
    'Trung bình mỗi ngày tôi dành ___ giờ cho Facebook/Instagram/TikTok.'
  ],
  'III': [
    'Gia đình tôi thường xuyên hỏi han, động viên tiến độ học tập hàng tuần.',
    'Áp lực tài chính (học phí, chi phí sinh hoạt) từ gia đình ảnh hưởng đến thời gian học của tôi.',
    'Sự hỗ trợ tinh thần từ gia đình giúp tôi vượt khó trong học tập.',
    'Môi trường sống xung quanh (khu ký túc xá, tổ dân phố) tạo điều kiện thuận lợi cho việc học.',
    'Các hoạt động xã hội (đoàn thể, tình nguyện) tôi tham gia ảnh hưởng đến lịch học và tự học.'
  ],
  'IV': [
    'Nhóm bạn thân thường xuyên thảo luận và giải quyết bài tập khó cùng tôi.',
    'Áp lực cạnh tranh thành tích với bạn bè khiến tôi nỗ lực hơn.',
    'Tôi dễ dàng tổ chức hoặc tham gia nhóm chat (Zalo/WhatsApp) để trao đổi bài tập.',
    'Mối quan hệ bạn bè tại HUMG tạo động lực tích cực cho việc học.',
    'Bạn bè của tôi chia sẻ nguồn tài liệu và mẹo ôn tập hữu ích.'
  ],
  'V': [
    'Thư viện HUMG có đủ đầu sách và giờ mở cửa linh hoạt phù hợp lịch học của tôi.',
    'Phòng máy tính & phòng thí nghiệm đủ thiết bị để tôi làm bài thực hành và dự án.',
    'Các câu lạc bộ học thuật (CNTT, Kinh tế, Ngoại ngữ…) tạo cơ hội rèn luyện kỹ năng chuyên môn.',
    'Không gian tự học (phòng tự học, góc học nhóm) trong khuôn viên trường yên tĩnh và thoải mái.',
    'Hệ thống LMS (Moodle/Google Classroom) của HUMG hoạt động ổn định, dễ truy cập.'
  ],
  'VI': [
    'Tôi lập kế hoạch chi tiết (lịch ôn, lịch nộp bài) cho mỗi môn học.',
    'Tôi hoàn thành nhiệm vụ học tập đúng hạn một cách tự giác.',
    'Tôi biết ưu tiên công việc học tập quan trọng trước.',
    'Tôi cân bằng tốt giữa thời gian học và các hoạt động khác.'
  ],
  'VII': [
    'Tôi chủ động tìm kiếm và sử dụng tài liệu ngoài giáo trình.',
    'Tôi ghi chú và hệ thống lại kiến thức ngay sau mỗi buổi học.',
    'Tôi tự đánh giá được mức độ hiểu bài và biết cách cải thiện.',
    'Tôi dễ dàng tự nghiên cứu khi gặp bài tập khó.'
  ],
  'VIII': [
    'Tôi tích cực tham gia thảo luận và chia sẻ ý kiến trong nhóm học.',
    'Tôi biết phân công và phối hợp hiệu quả với thành viên khác.',
    'Tôi lắng nghe và tiếp thu ý kiến đóng góp từ bạn bè.',
    'Tôi chủ động hỗ trợ đồng đội khi họ gặp khó khăn.'
  ],
  'IX': [
    'Tôi thường đặt câu hỏi "tại sao" để phân tích khái niệm mới.',
    'Tôi so sánh các giải pháp khác nhau để chọn cách tối ưu.',
    'Tôi biện luận có cơ sở khi tranh luận về nội dung học tập.',
    'Tôi kiểm tra và đánh giá tính chính xác của thông tin mình đọc.'
  ],
  'X': [
    'Tôi dễ dàng nắm bắt nội dung bài giảng mới và ứng dụng vào bài tập.',
    'Tôi biết tổng hợp thông tin từ nhiều nguồn để tạo hiểu biết sâu.',
    'Tôi sử dụng sơ đồ tư duy hoặc mindmap để tổ chức kiến thức.',
    'Tôi ôn tập định kỳ để duy trì và củng cố kiến thức đã học.'
  ]
};

const Survey = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(() => {
    const savedStep = localStorage.getItem('surveyActiveStep');
    return savedStep ? parseInt(savedStep) : 0;
  });
  
  const [formData, setFormData] = useState(() => {
    const savedFormData = localStorage.getItem('surveyFormData');
    return savedFormData ? JSON.parse(savedFormData) : {
      ho_va_ten: '',
      ma_so_sinh_vien: '',
      gioi_tinh: '',
      khoa: '',
      nam_hoc: '',
      social_media_hours: ''
    };
  });

  const [scores, setScores] = useState(() => {
    const savedScores = localStorage.getItem('surveyScores');
    return savedScores ? JSON.parse(savedScores) : {};
  });

  const [submitStatus, setSubmitStatus] = useState(null);
  const [sectionProgress, setSectionProgress] = useState(() => {
    const savedProgress = localStorage.getItem('surveyProgress');
    return savedProgress ? JSON.parse(savedProgress) : {};
  });
  const [validationErrors, setValidationErrors] = useState({});

  // Save data to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('surveyActiveStep', activeStep);
    localStorage.setItem('surveyFormData', JSON.stringify(formData));
    localStorage.setItem('surveyScores', JSON.stringify(scores));
    localStorage.setItem('surveyProgress', JSON.stringify(sectionProgress));
  }, [activeStep, formData, scores, sectionProgress]);

  // Clear localStorage after successful submission
  const clearLocalStorage = () => {
    localStorage.removeItem('surveyActiveStep');
    localStorage.removeItem('surveyFormData');
    localStorage.removeItem('surveyScores');
    localStorage.removeItem('surveyProgress');
  };

  const validatePersonalInfo = () => {
    const errors = {};
    if (!formData.ho_va_ten) errors.ho_va_ten = 'Vui lòng nhập họ tên';
    if (!formData.ma_so_sinh_vien) errors.ma_so_sinh_vien = 'Vui lòng nhập mã số sinh viên';
    if (!formData.gioi_tinh) errors.gioi_tinh = 'Vui lòng chọn giới tính';
    if (!formData.khoa) errors.khoa = 'Vui lòng chọn khoa';
    if (!formData.nam_hoc) errors.nam_hoc = 'Vui lòng chọn năm học';
    
    console.log('Personal info validation errors:', errors); // Debug log
    return errors;
  };

  const validateSection = (sectionKey) => {
    const errors = {};
    const questions = sectionQuestions[sectionKey];
    if (questions) {
      questions.forEach((_, index) => {
        if (sectionKey === 'II' && index === 4) {
          // Special validation for social media hours
          if (!formData.social_media_hours) {
            errors[`${sectionKey}_${index + 1}`] = 'Vui lòng chọn thời gian sử dụng mạng xã hội';
          }
        } else if (!scores[`${sectionKey}_${index + 1}`]) {
          errors[`${sectionKey}_${index + 1}`] = 'Vui lòng chọn một đáp án';
        }
      });
    }
    return errors;
  };

  const validateCurrentStep = () => {
    const currentSection = sections[activeStep];
    if (currentSection.key === 'A') {
      const errors = validatePersonalInfo();
      setValidationErrors(errors);
      return Object.keys(errors).length === 0;
    } else if (currentSection.key === 'II') {
      const errors = {
        ...validateSection(currentSection.key),
        ...(formData.social_media_hours ? {} : { social_media_hours: 'Vui lòng chọn thời gian sử dụng mạng xã hội' })
      };
      setValidationErrors(errors);
      return Object.keys(errors).length === 0;
    } else {
      const errors = validateSection(currentSection.key);
      setValidationErrors(errors);
      return Object.keys(errors).length === 0;
    }
  };

  const handlePersonalInfoChange = (e) => {
    const { name, value } = e.target;
    console.log('Form field changed:', name, value); // Debug log
    
    setFormData(prev => {
      const newData = {
        ...prev,
        [name]: value
      };
      console.log('Updated form data:', newData); // Debug log
      return newData;
    });

    // Clear validation error when user makes a change
    if (validationErrors[name]) {
      setValidationErrors(prev => ({
        ...prev,
        [name]: undefined
      }));
    }
  };

  const handleScoreChange = (section, question, value) => {
    const newScores = {
      ...scores,
      [`${section}_${question}`]: value
    };
    setScores(newScores);
    updateSectionProgress(section, newScores);
    // Clear validation error when user makes a selection
    if (validationErrors[`${section}_${question}`]) {
      setValidationErrors(prev => ({
        ...prev,
        [`${section}_${question}`]: undefined
      }));
    }
  };

  const updateSectionProgress = (section, currentScores) => {
    const sectionQuestions = getSectionQuestions(section);
    let answeredQuestions = 0;
    
    if (section === 'II') {
      // Special handling for Section II
      answeredQuestions = sectionQuestions.filter(q => {
        if (q === 5) {
          return formData.social_media_hours !== '';
        }
        return currentScores[`${section}_${q}`] !== undefined;
      }).length;
    } else {
      answeredQuestions = sectionQuestions.filter(q => 
        currentScores[`${section}_${q}`] !== undefined
      ).length;
    }
    
    const progress = (answeredQuestions / sectionQuestions.length) * 100;
    setSectionProgress(prev => ({
      ...prev,
      [section]: progress
    }));
  };

  const getSectionQuestions = (section) => {
    return Array.from({ length: sectionQuestions[section].length }, (_, i) => i + 1);
  };

  const handleNext = () => {
    if (validateCurrentStep()) {
      setActiveStep((prevStep) => prevStep + 1);
      setValidationErrors({});
      // Scroll to top of the page
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
    setValidationErrors({});
    // Scroll to top of the page
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateCurrentStep()) {
      try {
        // Log the current form data before submission
        console.log('Current form data before submission:', formData);

        // Ensure all required fields are present
        if (!formData.ma_so_sinh_vien || !formData.gioi_tinh || !formData.khoa || !formData.nam_hoc || !formData.ho_va_ten) {
          console.error('Missing required fields:', {
            ma_so_sinh_vien: formData.ma_so_sinh_vien,
            gioi_tinh: formData.gioi_tinh,
            khoa: formData.khoa,
            nam_hoc: formData.nam_hoc,
            ho_va_ten: formData.ho_va_ten
          });
          setSubmitStatus({ type: 'error', message: 'Vui lòng điền đầy đủ thông tin cá nhân.' });
          return;
        }

        // Create survey data with personal info at root level
        const surveyData = {
          ma_so_sinh_vien: formData.ma_so_sinh_vien,
          gioi_tinh: formData.gioi_tinh,
          khoa: formData.khoa,
          nam_hoc: formData.nam_hoc,
          ho_va_ten: formData.ho_va_ten
        };

        // Add all scores to the survey data
        Object.keys(scores).forEach(key => {
          surveyData[key] = scores[key];
        });

        console.log('Submitting survey data:', surveyData); // Debug log

        const response = await axios.post('http://localhost:5000/api/submit-survey', surveyData);
        console.log('Server response:', response.data); // Debug log
        
        setSubmitStatus({ type: 'success', message: 'Khảo sát đã được gửi thành công!' });
        clearLocalStorage();
        
        // Wait for 2 seconds to show the success message before navigating
        setTimeout(() => {
          navigate('/upload');
        }, 2000);
      } catch (error) {
        console.error('Error submitting survey:', error.response?.data || error); // Enhanced error logging
        setSubmitStatus({ type: 'error', message: 'Có lỗi xảy ra khi gửi khảo sát.' });
      }
    }
  };

  // Add a warning when trying to leave the page with unsaved data
  useEffect(() => {
    const handleBeforeUnload = (e) => {
      if (activeStep > 0 && !submitStatus?.type === 'success') {
        e.preventDefault();
        e.returnValue = '';
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, [activeStep, submitStatus]);

  const handleLogoClick = () => {
    navigate('/');
  };

  const renderQuestion = (section, questionNumber, questionText) => {
    const error = validationErrors[`${section}_${questionNumber}`];
    const isSocialMediaHours = section === 'II' && questionNumber === 5;

    return (
      <Fade in={true} timeout={500}>
        <Box 
          key={`${section}_${questionNumber}`} 
          sx={{ 
            mb: 3,
            p: 2,
            borderRadius: 2,
            bgcolor: alpha(theme.palette.primary.main, 0.05),
            transition: 'all 0.3s ease',
            border: error ? `1px solid ${theme.palette.error.main}` : 'none',
            '&:hover': {
              bgcolor: alpha(theme.palette.primary.main, 0.1),
              transform: 'translateX(8px)'
            }
          }}
        >
          <Typography variant="body1" sx={{ mb: 2, fontWeight: 500 }}>
            {questionNumber}. {isSocialMediaHours ? (
              <>
                Trung bình mỗi ngày tôi dành ___ giờ cho Facebook/Instagram/TikTok:
              </>
            ) : questionText}
          </Typography>
          {isSocialMediaHours ? (
            <FormControl component="fieldset" error={!!error}>
              <RadioGroup
                value={formData.social_media_hours}
                onChange={handlePersonalInfoChange}
                name="social_media_hours"
              >
                {[
                  { value: '5+', label: 'Lớn hơn 5 giờ' },
                  { value: '4', label: '4 giờ' },
                  { value: '3', label: '3 giờ' },
                  { value: '2', label: '2 giờ' },
                  { value: '1', label: '1 giờ' }
                ].map((option) => (
                  <FormControlLabel
                    key={option.value}
                    value={option.value}
                    control={<Radio />}
                    label={option.label}
                    sx={{
                      mb: 1,
                      transition: 'all 0.2s ease',
                      '&:hover': {
                        bgcolor: alpha(theme.palette.primary.main, 0.05),
                        borderRadius: 1
                      }
                    }}
                  />
                ))}
              </RadioGroup>
              {error && (
                <Typography color="error" variant="caption" sx={{ mt: 1, display: 'block' }}>
                  {error}
                </Typography>
              )}
            </FormControl>
          ) : (
            <FormControl component="fieldset" error={!!error}>
              <RadioGroup
                value={scores[`${section}_${questionNumber}`] || ''}
                onChange={(e) => handleScoreChange(section, questionNumber, e.target.value)}
              >
                {[1, 2, 3, 4, 5].map((value) => (
                  <FormControlLabel
                    key={value}
                    value={value.toString()}
                    control={<Radio />}
                    label={`${value} - ${
                      value === 1 ? 'Hoàn toàn không đồng ý' :
                      value === 2 ? 'Không đồng ý' :
                      value === 3 ? 'Phân vân' :
                      value === 4 ? 'Đồng ý' :
                      'Hoàn toàn đồng ý'
                    }`}
                    sx={{
                      mb: 1,
                      transition: 'all 0.2s ease',
                      '&:hover': {
                        bgcolor: alpha(theme.palette.primary.main, 0.05),
                        borderRadius: 1
                      }
                    }}
                  />
                ))}
              </RadioGroup>
              {error && (
                <Typography color="error" variant="caption" sx={{ mt: 1, display: 'block' }}>
                  {error}
                </Typography>
              )}
            </FormControl>
          )}
        </Box>
      </Fade>
    );
  };

  const renderSection = (title, sectionKey, questions) => {
    return (
      <Zoom in={true} timeout={500}>
        <Card 
          sx={{ 
            mb: 4, 
            boxShadow: 3,
            borderRadius: 2,
            overflow: 'hidden',
            transition: 'all 0.3s ease',
            '&:hover': {
              boxShadow: 6
            }
          }}
        >
          <CardContent>
            <Typography 
              variant="h6" 
              gutterBottom 
              sx={{ 
                color: theme.palette.primary.main,
                fontWeight: 'bold',
                mb: 3,
                pb: 2,
                borderBottom: `2px solid ${alpha(theme.palette.primary.main, 0.2)}`
              }}
            >
              {title}
            </Typography>
            <LinearProgress 
              variant="determinate" 
              value={sectionProgress[sectionKey] || 0}
              sx={{ 
                mb: 3, 
                height: 8, 
                borderRadius: 4,
                bgcolor: alpha(theme.palette.primary.main, 0.1),
                '& .MuiLinearProgress-bar': {
                  borderRadius: 4
                }
              }}
            />
            {questions.map((question, index) => (
              <Box key={index}>
                {renderQuestion(sectionKey, index + 1, question)}
              </Box>
            ))}
          </CardContent>
        </Card>
      </Zoom>
    );
  };

  const renderStepContent = (step) => {
    const currentSection = sections[step];
    
    if (currentSection.key === 'A') {
      return (
        <Zoom in={true} timeout={500}>
          <Card 
            sx={{ 
              mb: 4, 
              boxShadow: 3,
              borderRadius: 2,
              overflow: 'hidden',
              transition: 'all 0.3s ease',
              '&:hover': {
                boxShadow: 6
              }
            }}
          >
            <CardContent>
              <Typography 
                variant="h6" 
                gutterBottom 
                sx={{ 
                  color: theme.palette.primary.main,
                  fontWeight: 'bold',
                  mb: 3,
                  pb: 2,
                  borderBottom: `2px solid ${alpha(theme.palette.primary.main, 0.2)}`
                }}
              >
                A. Thông tin chung
              </Typography>
              <Box sx={{ mb: 3 }}>
                <TextField
                  fullWidth
                  label="Họ và tên"
                  name="ho_va_ten"
                  value={formData.ho_va_ten}
                  onChange={handlePersonalInfoChange}
                  error={!!validationErrors.ho_va_ten}
                  helperText={validationErrors.ho_va_ten}
                  sx={{ mb: 2 }}
                />
                <TextField
                  fullWidth
                  label="Mã số sinh viên"
                  name="ma_so_sinh_vien"
                  value={formData.ma_so_sinh_vien}
                  onChange={handlePersonalInfoChange}
                  error={!!validationErrors.ma_so_sinh_vien}
                  helperText={validationErrors.ma_so_sinh_vien}
                  sx={{ mb: 2 }}
                />
                <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                  <FormControl 
                    component="fieldset" 
                    error={!!validationErrors.gioi_tinh}
                    sx={{ flex: 1 }}
                  >
                    <FormLabel>Giới tính</FormLabel>
                    <RadioGroup
                      name="gioi_tinh"
                      value={formData.gioi_tinh}
                      onChange={handlePersonalInfoChange}
                    >
                      <FormControlLabel value="Nam" control={<Radio />} label="Nam" />
                      <FormControlLabel value="Nữ" control={<Radio />} label="Nữ" />
                      <FormControlLabel value="Khác" control={<Radio />} label="Khác" />
                    </RadioGroup>
                    {validationErrors.gioi_tinh && (
                      <Typography color="error" variant="caption" sx={{ mt: 1, display: 'block' }}>
                        {validationErrors.gioi_tinh}
                      </Typography>
                    )}
                  </FormControl>
                  <FormControl 
                    component="fieldset" 
                    error={!!validationErrors.khoa}
                    sx={{ flex: 1 }}
                  >
                    <FormLabel>Khoa</FormLabel>
                    <RadioGroup
                      name="khoa"
                      value={formData.khoa}
                      onChange={handlePersonalInfoChange}
                    >
                      <FormControlLabel value="Kinh tế" control={<Radio />} label="Kinh tế" />
                      <FormControlLabel value="Công nghệ Thông tin" control={<Radio />} label="Công nghệ Thông tin" />
                    </RadioGroup>
                    {validationErrors.khoa && (
                      <Typography color="error" variant="caption" sx={{ mt: 1, display: 'block' }}>
                        {validationErrors.khoa}
                      </Typography>
                    )}
                  </FormControl>
                </Box>
                <FormControl component="fieldset" error={!!validationErrors.nam_hoc}>
                  <FormLabel>Năm học hiện tại</FormLabel>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {[1, 2, 3, 4, 5].map((year) => (
                      <FormControlLabel
                        key={year}
                        control={
                          <Radio
                            checked={formData.nam_hoc === year.toString()}
                            onChange={handlePersonalInfoChange}
                            name="nam_hoc"
                            value={year.toString()}
                          />
                        }
                        label={year.toString()}
                        sx={{
                          m: 0,
                          px: 2,
                          py: 1,
                          border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
                          borderRadius: 1,
                          transition: 'all 0.2s ease',
                          '&:hover': {
                            bgcolor: alpha(theme.palette.primary.main, 0.05)
                          }
                        }}
                      />
                    ))}
                  </Box>
                  {validationErrors.nam_hoc && (
                    <Typography color="error" variant="caption" sx={{ mt: 1, display: 'block' }}>
                      {validationErrors.nam_hoc}
                    </Typography>
                  )}
                </FormControl>
              </Box>
            </CardContent>
          </Card>
        </Zoom>
      );
    }

    if (currentSection.key === 'II') {
      return (
        <>
          {renderSection(
            currentSection.label,
            currentSection.key,
            sectionQuestions[currentSection.key]
          )}
        </>
      );
    }

    return renderSection(
      currentSection.label,
      currentSection.key,
      sectionQuestions[currentSection.key]
    );
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

      {/* HUMG Logo */}
      <Box
        component={motion.div}
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8 }}
        onClick={handleLogoClick}
        sx={{
          position: 'absolute',
          top: 40,
          left: 40,
          zIndex: 1,
          cursor: 'pointer',
          '&:hover': {
            transform: 'scale(1.05)',
            transition: 'transform 0.2s ease-in-out'
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

      <Container maxWidth="md" sx={{ py: 4, position: 'relative', zIndex: 1 }}>
        <Paper 
          elevation={3} 
          sx={{ 
            p: 4, 
            borderRadius: 2,
            background: `linear-gradient(145deg, ${alpha(theme.palette.background.paper, 0.9)}, ${alpha(theme.palette.background.paper, 1)})`,
            mt: 8,
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
            Khảo sát yếu tố ảnh hưởng đến học tập
          </Typography>

          {submitStatus && (
            <Alert 
              severity={submitStatus.type} 
              sx={{ 
                mb: 2,
                borderRadius: 2
              }}
            >
              {submitStatus.message}
            </Alert>
          )}

          <Stepper 
            activeStep={activeStep} 
            alternativeLabel 
            sx={{ 
              mb: 4,
              '& .MuiStepLabel-label': {
                fontSize: '0.875rem'
              }
            }}
          >
            {sections.map((section) => (
              <Step key={section.key}>
                <StepLabel>{section.label}</StepLabel>
              </Step>
            ))}
          </Stepper>

          <form onSubmit={handleSubmit}>
            {renderStepContent(activeStep)}

            <Box 
              sx={{ 
                mt: 4, 
                display: 'flex', 
                justifyContent: 'space-between',
                gap: 2
              }}
            >
              <Button
                disabled={activeStep === 0}
                onClick={handleBack}
                variant="outlined"
                color="primary"
                sx={{
                  borderRadius: 2,
                  px: 4
                }}
              >
                Quay lại
              </Button>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={() => navigate('/upload')}
                  sx={{
                    borderRadius: 2,
                    px: 4,
                    borderWidth: 2,
                    '&:hover': {
                      borderWidth: 2,
                      bgcolor: alpha(theme.palette.primary.main, 0.1)
                    }
                  }}
                >
                  Upload File
                </Button>
                {activeStep === sections.length - 1 ? (
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    size="large"
                    sx={{
                      borderRadius: 2,
                      px: 4,
                      background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.primary.dark})`,
                      '&:hover': {
                        background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.primary.main})`
                      }
                    }}
                  >
                    Gửi khảo sát
                  </Button>
                ) : (
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleNext}
                    sx={{
                      borderRadius: 2,
                      px: 4,
                      background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.primary.dark})`,
                      '&:hover': {
                        background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.primary.main})`
                      }
                    }}
                  >
                    Tiếp tục
                  </Button>
                )}
              </Box>
            </Box>
          </form>
        </Paper>
      </Container>
    </Box>
  );
};

export default Survey; 