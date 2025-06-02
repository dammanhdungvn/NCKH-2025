# quick_response_templates.py - Template System cho Fast Responses
# 🚀 Hệ thống template thông minh cho educational patterns phổ biến

import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class QuickResponseTemplates:
    """
    Hệ thống template responses cho các patterns giáo dục phổ biến
    Giúp giảm thời gian phản hồi cho các trường hợp quen thuộc
    """
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.pattern_matchers = self._initialize_pattern_matchers()
        self.usage_stats = {}
        
    def _initialize_templates(self) -> Dict:
        """Initialize comprehensive template library"""
        return {
            # =================== ACADEMIC PERFORMANCE TEMPLATES ===================
            "excellent_performer": {
                "conditions": {
                    "skills_avg": {"min": 85},
                    "grades_avg": {"min": 85},
                    "grade_consistency": {"min": 0.8}
                },
                "template": """🌟 **PHÂN TÍCH NHANH - HỌC SINH XUẤT SẮC**

📊 **Profile Assessment:**
- Kỹ năng học tập: **Xuất sắc** ({skills_avg:.1f}%)
- Thành tích học tập: **Ưu tú** ({grades_avg:.1f}%)
- Tính nhất quán: **Cao** ({grade_consistency:.1f})

🎯 **Advanced Development Plan:**

**1. Leadership & Mentorship (Ưu tiên cao)**
   - Tham gia làm Teaching Assistant cho môn mạnh
   - Dẫn dắt study groups cho junior students
   - Apply làm mentor trong các chương trình tân sinh viên

**2. Research & Innovation**
   - Tìm hiểu cơ hội nghiên cứu khoa học với professors
   - Apply cho Summer Research Programs
   - Consider writing technical papers/articles

**3. Industry Connections**
   - Network với alumni và industry professionals
   - Attend conferences, seminars trong ngành {major}
   - Join professional associations

**4. Advanced Skill Building**
   - Master advanced tools/technologies in {major}
   - Pursue relevant certifications (AWS, Google, Microsoft, etc.)
   - Learn complementary skills (business, management)

⭐ **Next Steps (This Month):**
- [ ] Identify 1 research opportunity
- [ ] Connect with 2 industry professionals
- [ ] Apply for 1 leadership role
- [ ] Start 1 advanced certification

🚀 **Career Acceleration:** Với profile này, bạn sẵn sàng cho top-tier opportunities. Focus vào building personal brand và networking.

⏱️ *Quick Response - Request full consultation for detailed 5-year roadmap*""",
                "confidence": 92
            },
            
            "struggling_student": {
                "conditions": {
                    "skills_avg": {"max": 50},
                    "grade_count_below_c": {"min": 3}
                },
                "template": """💪 **PHÂN TÍCH NHANH - RECOVERY & SUPPORT PLAN**

📊 **Current Situation:**
- Kỹ năng cần cải thiện: **{weak_skills}**
- Môn học cần attention: **{weak_subjects}**
- GPA hiện tại: **{current_gpa}** (cần nâng lên ≥2.5)

🎯 **Emergency Recovery Plan:**

**Week 1-2: Foundation Reset**
   - [ ] Meet với academic advisor ngay
   - [ ] Schedule tutoring cho 2 môn yếu nhất
   - [ ] Join study groups (tìm trên Facebook/Discord khoa)
   - [ ] Setup daily study schedule (6-8 hours/day)

**Week 3-4: Skills Building**
   - [ ] Apply Pomodoro Technique (25min focus + 5min break)
   - [ ] Practice active recall thay vì passive reading
   - [ ] Use spaced repetition cho memorization
   - [ ] Find accountability partner

**Month 2-3: Performance Improvement**
   - [ ] Target grade B cho môn dễ nhất để boost confidence
   - [ ] Improve time management với calendar blocking
   - [ ] Develop note-taking system (Cornell/Mind mapping)
   - [ ] Regular check-ins với professors

**🆘 Immediate Support Resources:**
- **Academic Support Center**: Tutoring, study skills workshops
- **Counseling Services**: Stress management, motivation
- **Peer Support**: Study buddy, senior mentors
- **Family Support**: Open communication about challenges

📈 **Goal Timeline:**
- **Next exam**: Aim for 1 grade level improvement
- **End of semester**: Achieve minimum 2.5 GPA
- **Next semester**: Build momentum với balanced course load

⚠️ **Red Flags to Monitor:**
- Skipping classes (attendance >90% critical)
- Procrastination patterns
- Sleep/health issues
- Social isolation

⏱️ *Quick Response - Request full consultation for personalized recovery strategy*""",
                "confidence": 88
            },
            
            "balanced_student": {
                "conditions": {
                    "skills_avg": {"min": 60, "max": 84},
                    "grades_avg": {"min": 70, "max": 84}
                },
                "template": """⚖️ **PHÂN TÍCH NHANH - OPTIMIZATION STRATEGY**

📊 **Current Performance:**
- Overall Skills: **Good** ({skills_avg:.1f}%)
- Academic Performance: **Satisfactory** ({grades_avg:.1f}%)
- Growth Potential: **High** 🎯

🎯 **Strategic Optimization Plan:**

**Phase 1: Identify & Leverage Strengths (Month 1)**
   - Top 3 strongest skills: **{top_skills}**
   - Best performing subjects: **{best_subjects}**
   - Action: Build expertise trong 1-2 areas này

**Phase 2: Address Key Gaps (Month 2-3)**
   - Priority improvement areas: **{weak_areas}**
   - Specific actions:
     * {improvement_plan}
   - Target: Raise weakest areas to 70%+ level

**Phase 3: Advanced Development (Month 4-6)**
   - [ ] Apply for internship/part-time relevant job
   - [ ] Join 1 professional club/organization
   - [ ] Start portfolio/personal project
   - [ ] Network với seniors và alumni

**🎯 SMART Goals cho semester này:**
- **Academic**: Maintain current strong subjects, improve 2 weakest by 1 grade level
- **Skills**: Focus on {priority_skill_1} và {priority_skill_2}
- **Experience**: Gain 1 practical experience (internship/project)
- **Network**: Connect với 5 professionals trong field

**📈 Growth Trajectory:**
```
Current Level: Good (B-B+ range)
6-month Goal: Very Good (A-A- range)  
1-year Goal: Excellent với leadership experience
```

**💡 Pro Tips:**
- Use "Good Student Advantage": Professors notice consistent performers
- Leverage peer network: Good students often have great connections
- Balance risk: Try 1 challenging course while maintaining stability

⏱️ *Quick Response - Request full consultation for detailed semester planning*""",
                "confidence": 85
            },
            
            # =================== MAJOR-SPECIFIC TEMPLATES ===================
            "computer_science_guidance": {
                "conditions": {
                    "major": ["CNTT", "Khoa học máy tính", "Công nghệ thông tin"]
                },
                "template": """💻 **CS/IT STUDENT QUICK GUIDANCE**

**Technical Skills Roadmap:**
- **Fundamentals**: Data Structures, Algorithms, OOP
- **Web Development**: HTML/CSS/JS → React/Vue → Backend (Node.js/Python)
- **Database**: SQL fundamentals → MongoDB/PostgreSQL
- **DevOps**: Git/GitHub → Docker → CI/CD basics

**Industry-Ready Projects:**
1. **Full-stack Web App** (e-commerce, social platform)
2. **Mobile App** (React Native/Flutter)
3. **Data Analysis Project** (Python/pandas)
4. **Open Source Contribution**

**Certification Priorities:**
- Cloud: AWS/Google Cloud fundamentals
- Frameworks: React, Node.js certificates
- Specialization: AI/ML, Cybersecurity, or DevOps

**Job Market Strategy:**
- Build strong GitHub portfolio
- Practice coding interviews (LeetCode, HackerRank)
- Network trên LinkedIn, attend tech meetups
- Apply for internships at startups + big tech

⏱️ *CS-specific template - Request full consultation for detailed technical roadmap*""",
                "confidence": 90
            },
            
            "business_economics_guidance": {
                "conditions": {
                    "major": ["Kinh tế", "Quản trị kinh doanh", "Tài chính"]
                },
                "template": """📈 **BUSINESS/ECONOMICS QUICK GUIDANCE**

**Core Competencies to Develop:**
- **Analytical Skills**: Excel advanced, SQL basics, Power BI
- **Communication**: Presentation skills, report writing
- **Business Acumen**: Market analysis, financial modeling
- **Soft Skills**: Leadership, negotiation, project management

**Career Path Options:**
1. **Corporate Finance**: Banking, investment, corporate FP&A
2. **Consulting**: Management consulting, business analysis
3. **Marketing**: Digital marketing, brand management
4. **Entrepreneurship**: Startup, business development

**Practical Experience:**
- Join business clubs, case competitions
- Seek internships in banking/consulting
- Volunteer for NGO financial projects
- Start small business/side hustle

**Professional Development:**
- CFA Level 1 (Finance track)
- Google Analytics/Ads (Marketing track)
- Project Management certification
- Industry-specific courses (banking, consulting)

⏱️ *Business-specific template - Request full consultation for career pathway planning*""",
                "confidence": 88
            },
            
            # =================== SKILL-SPECIFIC TEMPLATES ===================
            "time_management_improvement": {
                "conditions": {
                    "weak_skill": "Quan_ly_thoi_gian",
                    "skill_score": {"max": 60}
                },
                "template": """⏰ **TIME MANAGEMENT MASTERY PLAN**

**Immediate Fixes (This Week):**
- [ ] Download calendar app (Google Calendar/Notion)
- [ ] Time-block daily schedule (include study, rest, meals)
- [ ] Set 3 daily priorities using Eisenhower Matrix
- [ ] Use Pomodoro Timer (25min work + 5min break)

**System Setup (Week 2-3):**
- [ ] Weekly planning sessions (Sunday 30min)
- [ ] Daily reviews (10min before bed)
- [ ] Batch similar tasks together
- [ ] Create buffer time for unexpected events

**Advanced Strategies (Month 2):**
- [ ] Track time for 1 week to identify patterns
- [ ] Eliminate/delegate low-value activities
- [ ] Setup automated systems (bill pay, meal prep)
- [ ] Practice saying "no" to non-essential commitments

**Productivity Tools:**
- **Planning**: Notion, Todoist, or simple paper planner
- **Time Tracking**: Toggl, RescueTime
- **Focus**: Forest app, Freedom (block distractions)
- **Habits**: Habitica, Streaks

⏱️ *Time Management template - Achieve 80%+ efficiency in 30 days*""",
                "confidence": 92
            },
            
            "study_skills_enhancement": {
                "conditions": {
                    "weak_skill": "Tu_hoc",
                    "skill_score": {"max": 65}
                },
                "template": """📚 **STUDY SKILLS TRANSFORMATION**

**Learning System Upgrade:**

**1. Active Learning Techniques:**
- **Feynman Technique**: Explain concepts in simple terms
- **Active Recall**: Test yourself without looking at notes
- **Spaced Repetition**: Review material at increasing intervals
- **Interleaving**: Mix different topics in single study session

**2. Note-Taking Revolution:**
- **Cornell Method**: Divide page into notes, cues, summary
- **Mind Mapping**: Visual connections between concepts
- **Digital Tools**: Notion, Obsidian for linked knowledge

**3. Memory Enhancement:**
- **Mnemonics**: Create memorable acronyms/stories
- **Visualization**: Convert abstract concepts to images
- **Chunking**: Break complex info into smaller pieces
- **Practice Testing**: Weekly self-quizzes

**4. Environment Optimization:**
- **Study Space**: Dedicated, distraction-free zone
- **Lighting**: Natural light or warm LED (not blue)
- **Music**: Instrumental/nature sounds or silence
- **Breaks**: 5-10min every 25-45min study

**Study Schedule Template:**
```
📅 Daily: 3-4 focused study blocks
🔄 Weekly: Review previous week's material
📝 Monthly: Comprehensive self-testing
```

⏱️ *Study Skills template - Master efficient learning in 3 weeks*""",
                "confidence": 90
            }
        }
    
    def _initialize_pattern_matchers(self) -> Dict:
        """Initialize pattern matching functions"""
        return {
            "academic_level": self._match_academic_level,
            "major_specific": self._match_major,
            "skill_specific": self._match_weak_skills,
            "grade_pattern": self._match_grade_pattern
        }
    
    def _match_academic_level(self, data: Dict) -> List[str]:
        """Match academic performance level"""
        matches = []
        skills_avg = data.get("skills_avg", 0)
        grades_avg = data.get("grades_avg", 0)
        
        if skills_avg >= 85 and grades_avg >= 85:
            matches.append("excellent_performer")
        elif skills_avg < 50 or grades_avg < 60:
            matches.append("struggling_student")
        elif 60 <= skills_avg < 85 and 70 <= grades_avg < 85:
            matches.append("balanced_student")
        
        return matches
    
    def _match_major(self, data: Dict) -> List[str]:
        """Match major-specific guidance"""
        major = data.get("major", "").lower()
        matches = []
        
        cs_keywords = ["cntt", "công nghệ thông tin", "khoa học máy tính", "computer", "software"]
        business_keywords = ["kinh tế", "quản trị", "tài chính", "marketing", "business"]
        
        if any(keyword in major for keyword in cs_keywords):
            matches.append("computer_science_guidance")
        elif any(keyword in major for keyword in business_keywords):
            matches.append("business_economics_guidance")
        
        return matches
    
    def _match_weak_skills(self, data: Dict) -> List[str]:
        """Match skill-specific improvements"""
        matches = []
        weak_skills = data.get("weak_skills_detail", {})
        
        for skill, score in weak_skills.items():
            if skill == "Quan_ly_thoi_gian" and score < 60:
                matches.append("time_management_improvement")
            elif skill == "Tu_hoc" and score < 65:
                matches.append("study_skills_enhancement")
        
        return matches
    
    def _match_grade_pattern(self, data: Dict) -> List[str]:
        """Match based on grade patterns"""
        matches = []
        grade_distribution = data.get("grade_distribution", {})
        
        # Count grades below C
        below_c_count = grade_distribution.get("D", 0) + grade_distribution.get("F", 0)
        if below_c_count >= 3:
            matches.append("struggling_student")
        
        return matches
    
    def find_matching_templates(self, analysis_data: Dict) -> List[Tuple[str, Dict, float]]:
        """
        Find all templates that match the current student data
        Returns: List of (template_name, template_data, match_confidence)
        """
        matches = []
        
        for template_name, template_data in self.templates.items():
            confidence = self._calculate_match_confidence(analysis_data, template_data)
            if confidence > 70:  # Threshold for template usage
                matches.append((template_name, template_data, confidence))
        
        # Sort by confidence
        matches.sort(key=lambda x: x[2], reverse=True)
        return matches
    
    def _calculate_match_confidence(self, data: Dict, template: Dict) -> float:
        """Calculate how well data matches template conditions"""
        conditions = template.get("conditions", {})
        if not conditions:
            return 0
        
        matched_conditions = 0
        total_conditions = len(conditions)
        
        for condition_key, condition_value in conditions.items():
            if self._check_condition(data, condition_key, condition_value):
                matched_conditions += 1
        
        base_confidence = (matched_conditions / total_conditions) * 100
        
        # Boost confidence for exact matches
        if matched_conditions == total_conditions:
            base_confidence = min(100, base_confidence * 1.1)
        
        return base_confidence
    
    def _check_condition(self, data: Dict, condition_key: str, condition_value) -> bool:
        """Check if a specific condition is met"""
        try:
            if condition_key == "major":
                student_major = data.get("major", "").lower()
                return any(major.lower() in student_major for major in condition_value)
            
            elif condition_key == "weak_skill":
                weak_skills = data.get("weak_skills_detail", {})
                return condition_value in weak_skills
            
            elif condition_key in ["skills_avg", "grades_avg", "grade_consistency"]:
                value = data.get(condition_key, 0)
                if isinstance(condition_value, dict):
                    min_val = condition_value.get("min", float("-inf"))
                    max_val = condition_value.get("max", float("inf"))
                    return min_val <= value <= max_val
                else:
                    return value >= condition_value
            
            elif condition_key == "skill_score":
                # This should be checked in context of specific skill
                return True  # Will be handled by weak_skill condition
            
            elif condition_key == "grade_count_below_c":
                count = data.get("grade_count_below_c", 0)
                if isinstance(condition_value, dict):
                    min_val = condition_value.get("min", 0)
                    return count >= min_val
                else:
                    return count >= condition_value
            
            return False
            
        except Exception:
            return False
    
    def generate_quick_response(self, analysis_data: Dict, 
                               template_name: str = None) -> Optional[Dict]:
        """
        Generate quick response using best matching template
        """
        if template_name and template_name in self.templates:
            # Use specific template
            template = self.templates[template_name]
            confidence = template.get("confidence", 75)
        else:
            # Find best matching template
            matches = self.find_matching_templates(analysis_data)
            if not matches:
                return None
            
            template_name, template, confidence = matches[0]
        
        # Fill template with data
        filled_template = self._fill_template(template["template"], analysis_data)
        
        # Update usage stats
        if template_name not in self.usage_stats:
            self.usage_stats[template_name] = {"count": 0, "total_confidence": 0}
        
        self.usage_stats[template_name]["count"] += 1
        self.usage_stats[template_name]["total_confidence"] += confidence
        
        return {
            "template_name": template_name,
            "response": filled_template,
            "confidence": confidence,
            "generated_at": datetime.now().isoformat(),
            "source": "quick_template"
        }
    
    def _fill_template(self, template_text: str, data: Dict) -> str:
        """Fill template placeholders with actual data"""
        try:
            # Prepare formatting data
            format_data = {
                "skills_avg": data.get("skills_avg", 0),
                "grades_avg": data.get("grades_avg", 0),
                "grade_consistency": data.get("grade_consistency", 0),
                "major": data.get("major", "Unknown"),
                "current_gpa": data.get("current_gpa", "N/A"),
                "weak_skills": ", ".join(data.get("weak_skills", [])[:3]),
                "weak_subjects": ", ".join(data.get("weak_subjects", [])[:3]),
                "best_subjects": ", ".join(data.get("best_subjects", [])[:3]),
                "top_skills": ", ".join(data.get("top_skills", [])[:3]),
                "weak_areas": ", ".join(data.get("weak_areas", [])[:3]),
                "improvement_plan": self._generate_improvement_plan(data),
                "priority_skill_1": data.get("priority_skills", ["Communication"])[0] if data.get("priority_skills") else "Communication",
                "priority_skill_2": data.get("priority_skills", ["Critical Thinking", "Time Management"])[1] if len(data.get("priority_skills", [])) > 1 else "Time Management"
            }
            
            return template_text.format(**format_data)
            
        except Exception as e:
            print(f"Error filling template: {e}")
            return template_text  # Return unfilled template if error
    
    def _generate_improvement_plan(self, data: Dict) -> str:
        """Generate specific improvement plan based on weak areas"""
        weak_skills = data.get("weak_skills_detail", {})
        plans = []
        
        for skill, score in list(weak_skills.items())[:2]:  # Top 2 weak skills
            if skill == "Quan_ly_thoi_gian":
                plans.append("Daily scheduling với time-blocking technique")
            elif skill == "Tu_hoc":
                plans.append("Active recall và spaced repetition")
            elif skill == "Tu_duy_phan_bien":
                plans.append("Critical thinking exercises và case studies")
            elif skill == "Hop_tac_nhom":
                plans.append("Join study groups và team projects")
            else:
                plans.append(f"Targeted practice in {skill.replace('_', ' ').lower()}")
        
        return "\n     * ".join(plans) if plans else "Focus on consistent practice and seeking feedback"
    
    def get_usage_statistics(self) -> Dict:
        """Get template usage statistics"""
        stats = {}
        for template_name, usage in self.usage_stats.items():
            avg_confidence = usage["total_confidence"] / max(1, usage["count"])
            stats[template_name] = {
                "usage_count": usage["count"],
                "average_confidence": round(avg_confidence, 1),
                "last_used": "N/A"  # Could track this if needed
            }
        
        return {
            "template_stats": stats,
            "total_templates": len(self.templates),
            "total_quick_responses": sum(usage["count"] for usage in self.usage_stats.values())
        }

# Global template system instance
quick_templates = QuickResponseTemplates()
