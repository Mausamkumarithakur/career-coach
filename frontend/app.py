import streamlit as st
import requests
import json
from pypdf import PdfReader
import os

# Page config
st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    
    .header {
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    .header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 10px;
    }
    
    .upload-box {
        border: 3px dashed #2563EB;
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        background: white;
        transition: all 0.3s ease;
    }
    
    .upload-box:hover {
        border-color: #1E40AF;
        background: #EFF6FF;
    }
    
    .upload-box h3 {
        color: #2563EB;
        margin-bottom: 10px;
    }
    
    .upload-box p {
        color: #6B7280;
    }
    
    .card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }
    
    .card h3 {
        color: #1F2937;
        margin-top: 0;
        border-bottom: 2px solid #2563EB;
        padding-bottom: 10px;
    }
    
    .score-badge {
        display: inline-block;
        background: #2563EB;
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .question-card {
        background: white;
        border-left: 4px solid #2563EB;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .question-card h4 {
        color: #1F2937;
        margin-top: 0;
    }
    
    .question-card .why-asked {
        background: #EFF6FF;
        padding: 10px;
        border-radius: 6px;
        font-size: 0.9rem;
        color: #1E40AF;
    }
    
    .question-card .sample-answer {
        background: #F0FDF4;
        padding: 10px;
        border-radius: 6px;
        font-size: 0.9rem;
        color: #166534;
    }
    
    .about-hero {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        color: white;
        padding: 40px;
        border-radius: 12px;
        margin-bottom: 30px;
    }
    
    .about-hero h2 {
        margin: 0 0 15px 0;
    }
    
    .mission-card {
        background: white;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }
    
    .steps-container {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .step-card {
        flex: 1;
        background: white;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .step-number {
        background: #2563EB;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin: 0 auto 15px auto;
    }
    
    .tech-stack {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 15px;
    }
    
    .tech-badge {
        background: #EFF6FF;
        color: #2563EB;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        color: #6B7280;
        border-top: 1px solid #E5E7EB;
    }
    
    .stButton > button {
        background: #2563EB;
        color: white;
        border: none;
        padding: 10px 30px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #1E40AF;
        transform: translateY(-2px);
    }
    
    .feedback-card {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 4px solid;
    }
    
    .feedback-card.green {
        background: #F0FDF4;
        border-left-color: #16A34A;
    }
    
    .feedback-card.yellow {
        background: #FFFBEB;
        border-left-color: #F59E0B;
    }
    
    .feedback-card.red {
        background: #FEF2F2;
        border-left-color: #DC2626;
    }
    
    .feedback-card h4 {
        margin-top: 0;
    }
    
    .loading {
        text-align: center;
        padding: 40px;
    }
    
    .loading p {
        color: #6B7280;
        font-size: 1.1rem;
    }
    
    @media (max-width: 768px) {
        .header h1 {
            font-size: 1.8rem;
        }
        
        .steps-container {
            flex-direction: column;
        }
        
        .tab-button {
            padding: 10px 20px;
            font-size: 0.9rem;
        }
        
        .upload-box {
            padding: 25px;
        }
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = "http://localhost:8000"

# Header Section
st.markdown("""
<div class="header">
    <h1>🚀 AI Career Coach</h1>
    <p>Helping Tier-3 Students Get Hired with AI-Powered Guidance</p>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📄 Resume Analysis", "🎯 Interview Questions", "📚 Skill Roadmap", "ℹ️ About"])

# ==================== TAB 1: RESUME ANALYSIS ====================
with tab1:
    st.markdown("### 📄 Resume Analyzer")
    st.markdown("Upload your resume to get AI-powered feedback and improve your chances of getting hired.")
    
    # Upload Section
    uploaded_file = st.file_uploader("Drag & Drop Resume PDF Here", type=["pdf"], help="Supports PDF files only")
    
    if uploaded_file:
        # Show file info
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Extract text from PDF
        try:
            reader = PdfReader(uploaded_file)
            resume_text = ""
            for page in reader.pages:
                 text = page.extract_text()
                 if text:
                      resume_text += text
            if not resume_text.strip():
                 st.error("Could not extract text from this PDF. Try another resume.")
                 st.stop()
            
            # Job Description Input
            job_desc = st.text_area(
                "Optional: Paste Job Description (for better analysis)",
                height=150,
                placeholder="e.g., We are looking for a Python Developer with 2 years experience...",
                help="Adding JD helps us give more targeted feedback"
            )
            
            if st.button("🔍 Analyze Resume", use_container_width=True):
                with st.spinner("⏳ Analyzing your resume..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/analyze-resume",
                            json={
                                "resume_text": resume_text,
                                "job_description": job_desc
                            },
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            # Score Section
                            st.markdown("### 📊 Resume Score")
                            score = result.get("score", 0)
                            col1, col2, col3 = st.columns([1, 2, 1])
                            with col2:
                                st.markdown(f"""
                                <div style="text-align: center;">
                                    <div class="score-badge">{score}/100</div>
                                    <p style="color: #6B7280; margin-top: 10px;">Based on ATS standards</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.divider()
                            
                            # Feedback Cards
                            st.markdown("### 💡 Feedback")
                            
                            # Strengths
                            strengths = result.get("strengths", [])
                            if strengths:
                                st.markdown("#### 🟢 Strengths")
                                for strength in strengths:
                                    st.markdown(f"""
                                    <div class="feedback-card green">
                                        <h4>✅ {strength}</h4>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            # Improvements
                            improvements = result.get("improvements", [])
                            if improvements:
                                st.markdown("#### 🟡 Improvements")
                                for imp in improvements:
                                    st.markdown(f"""
                                    <div class="feedback-card yellow">
                                        <h4>📝 {imp}</h4>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            # Missing Sections
                            missing = result.get("missing_sections", [])
                            if missing:
                                st.markdown("#### 🔴 Missing Sections")
                                for miss in missing:
                                    st.markdown(f"""
                                    <div class="feedback-card red">
                                        <h4>⚠️ {miss}</h4>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            # Missing Keywords
                            keywords = result.get("missing_keywords", [])
                            if keywords:
                                st.markdown("#### 🔑 Missing Keywords")
                                st.write(", ".join(keywords))
                            
                            # Overall Advice
                            advice = result.get("overall_advice", "")
                            if advice:
                                st.markdown("### 📝 Overall Advice")
                                st.info(advice)
                            
                        else:
                            st.error(f"Error: {response.text}")
                    
                    except Exception as e:
                        st.error(f"Connection Error: {str(e)}")
                        st.info("Make sure the backend server is running on port 8000")
        
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")

# ==================== TAB 2: INTERVIEW QUESTIONS ====================
with tab2:
    st.markdown("### 🎯 Interview Question Generator")
    st.markdown("Get role-specific interview questions to prepare for your next interview.")
    
    # Input Fields
    col1, col2 = st.columns(2)
    
    with col1:
        role = st.text_input("💼 Job Role", placeholder="e.g., Python Developer", help="Enter the job role you're applying for")
    
    with col2:
        experience = st.selectbox(
            "🧠 Experience Level",
            ["Fresher", "1-2 Years", "3-5 Years", "5+ Years"],
            help="Select your experience level"
        )
    
    if st.button("🔍 Generate Questions", use_container_width=True):
        if role:
            with st.spinner("⏳ Generating interview questions..."):
                try:
                    response = requests.post(
                        f"{API_URL}/generate-interview-questions",
                        json={
                            "role": role,
                            "experience": experience
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        questions = result.get("questions", [])
                        
                        # Display Questions
                        st.markdown("### 📋 Generated Questions")
                        
                        if questions and isinstance(questions, list):
                            for i, q in enumerate(questions, 1):
                                st.markdown(f"""
                                <div class="question-card">
                                    <h4>Question {i}: {q.get('question', 'N/A')}</h4>
                                    <div class="why-asked">
                                        <strong>🧠 Why This is Asked:</strong> {q.get('why_asked', 'N/A')}
                                    </div>
                                    <div class="sample-answer">
                                        <strong>💡 Sample Answer:</strong> {q.get('sample_answer', 'N/A')}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Regenerate Button
                            if st.button("🔁 Regenerate Questions", use_container_width=True):
                                st.rerun()
                        else:
                            st.warning("No questions generated. Please try again.")
                    
                    else:
                        st.error(f"Error: {response.text}")
                
                except Exception as e:
                    st.error(f"Connection Error: {str(e)}")
                    st.info("Make sure the backend server is running on port 8000")
        else:
            st.warning("Please enter a job role!")

# ==================== TAB 3: SKILL ROADMAP ====================
with tab3:
    st.markdown("### 📚 Skill Roadmap Generator")
    st.markdown("Get a personalized learning path for your target role.")
    
    # Input Fields
    col1, col2 = st.columns(2)
    
    with col1:
        role = st.text_input("💼 Target Role", placeholder="e.g., Python Developer", help="Enter the job role you want to learn")
    
    with col2:
        experience = st.selectbox(
            "🧠 Current Experience",
            ["Fresher", "1-2 Years", "3-5 Years", "5+ Years"],
            help="Select your current experience level"
        )
    
    # Initialize session state
    if "roadmap_data" not in st.session_state:
        st.session_state.roadmap_data = ""
    if "roadmap_role" not in st.session_state:
        st.session_state.roadmap_role = ""
    
    if st.button("🔍 Generate Roadmap", use_container_width=True):
        if role:
            with st.spinner("⏳ Creating your personalized roadmap..."):
                try:
                    response = requests.post(
                        f"{API_URL}/generate-skill-roadmap",
                        json={
                            "role": role,
                            "experience": experience
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        roadmap_data = result.get("roadmap", "")
                        
                        # Store in session state
                        st.session_state.roadmap_data = roadmap_data
                        st.session_state.roadmap_role = role
                        
                        # Display Roadmap
                        st.markdown("### 📋 Your Learning Path")
                        st.markdown(roadmap_data)
                        
                    else:
                        st.error(f"Error: {response.text}")
                
                except Exception as e:
                    st.error(f"Connection Error: {str(e)}")
                    st.info("Make sure the backend server is running on port 8000")
        else:
            st.warning("Please enter a target role!")
    
    # Download Button (Only shows if roadmap_data exists)
    if st.session_state.roadmap_data:
        st.download_button(
            label="📄 Download Roadmap as Text",
            data=st.session_state.roadmap_data,
            file_name=f"{st.session_state.roadmap_role}_roadmap.txt",
            mime="text/plain",
            use_container_width=True
        )

# ==================== TAB 4: ABOUT ====================
with tab4:
    # Hero Section
    st.markdown("""
    <div class="about-hero">
        <h2>🚀 About AI Career Coach</h2>
        <p>AI Career Coach is designed to help students and freshers prepare for jobs with smart resume feedback and personalized interview questions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mission Section
    st.markdown("### 🎯 Our Mission")
    st.markdown("""
    <div class="mission-card">
        <h3 style="color: #2563EB; margin-top: 0;">To Empower Tier-2 and Tier-3 Students</h3>
        <p style="font-size: 1.1rem; color: #374151;">
            We believe every student deserves access to quality career guidance. 
            Our AI-powered platform helps students from all backgrounds prepare 
            confidently for interviews and build strong resumes without expensive consultants.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # How It Works (3 Steps)
    st.markdown("### 📋 How It Works")
    st.markdown("""
    <div class="steps-container">
        <div class="step-card">
            <div class="step-number">1</div>
            <h4>Upload Resume</h4>
            <p style="color: #6B7280;">Upload your current resume in PDF format</p>
        </div>
        <div class="step-card">
            <div class="step-number">2</div>
            <h4>AI Analyzes</h4>
            <p style="color: #6B7280;">Our AI evaluates your resume against industry standards</p>
        </div>
        <div class="step-card">
            <div class="step-number">3</div>
            <h4>Get Feedback</h4>
            <p style="color: #6B7280;">Receive personalized improvements and interview tips</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Tech Stack Section
    st.markdown("### 🛠 Built With")
    st.markdown("""
    <div class="tech-stack">
        <span class="tech-badge">🐍 Python</span>
        <span class="tech-badge">🤖 Llama 3</span>
        <span class="tech-badge">⚡ FastAPI</span>
        <span class="tech-badge">🎨 Streamlit</span>
        <span class="tech-badge">📄 PDF Parsing</span>
        <span class="tech-badge">🔒 Secure</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Made with ❤️ by <strong>Mousam Thakur</strong></p>
        <p style="font-size: 0.9rem; margin-top: 10px;">
            Helping students get hired, one resume at a time.
        </p>
    </div>
    """, unsafe_allow_html=True)
                                