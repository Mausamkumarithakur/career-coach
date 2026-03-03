from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq
from resume_parser import extract_text_from_pdf, clean_text, validate_resume_text
from prompts import RESUME_ANALYSIS_PROMPT, INTERVIEW_QUESTION_PROMPT, SKILL_ROADMAP_PROMPT
import json
import re

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ================= MODELS ================= #

class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str = ""

class InterviewRequest(BaseModel):
    role: str
    experience: str = "Fresher"

class SkillRequest(BaseModel):
    role: str
    experience: str = "Fresher"


# ================= JSON SAFE PARSER ================= #

def extract_json(content: str):
    """Safely extract JSON from LLM response"""
    try:
        content = re.sub(r'```json', '', content)
        content = re.sub(r'```', '', content)
        content = content.strip()

        json_match = re.search(r'\{.*\}', content, re.DOTALL)

        if not json_match:
            raise ValueError("No valid JSON found in response")

        json_string = json_match.group()
        return json.loads(json_string)

    except Exception as e:
        raise ValueError(f"JSON parsing failed: {str(e)}")


# ================= RESUME ANALYSIS ================= #

@app.post("/analyze-resume")
async def analyze_resume(request: ResumeRequest):
    try:
        is_valid, message = validate_resume_text(request.resume_text)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)

        prompt = RESUME_ANALYSIS_PROMPT + f"\n\nResume Text:\n{request.resume_text}"
        if request.job_description:
            prompt += f"\n\nJob Description:\n{request.job_description}"

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful career assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1200
        )

        content = response.choices[0].message.content
        result = extract_json(content)

        return result

    except Exception as e:
        return {
            "score": 70,
            "strengths": ["Resume processed successfully"],
            "improvements": ["Try uploading again"],
            "missing_sections": [],
            "missing_keywords": [],
            "overall_advice": f"Error occurred: {str(e)}"
        }


# ================= INTERVIEW QUESTIONS ================= #

@app.post("/generate-interview-questions")
async def generate_interview_questions(request: InterviewRequest):
    try:
        prompt = INTERVIEW_QUESTION_PROMPT.format(
            role=request.role,
            experience=request.experience
        )
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an interview coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        
        # Clean the content
        content = content.strip()
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```', '', content)
        content = content.strip()
        
        # Try to parse as JSON array
        try:
            questions = json.loads(content)
        except:
            # Fallback: create default questions
            questions = [
                {
                    "question": f"Tell me about yourself as a {request.role}.",
                    "why_asked": "Standard opening question to assess communication skills.",
                    "sample_answer": "Brief introduction about your background, skills, and career goals."
                },
                {
                    "question": "What are your strengths and weaknesses?",
                    "why_asked": "To understand self-awareness and honesty.",
                    "sample_answer": "Mention 2-3 strengths and 1 weakness with improvement plan."
                },
                {
                    "question": "Why do you want to work for our company?",
                    "why_asked": "To check company research and motivation.",
                    "sample_answer": "Mention company values, growth opportunities, and alignment with goals."
                },
                {
                    "question": "Where do you see yourself in 5 years?",
                    "why_asked": "To assess career planning and commitment.",
                    "sample_answer": "Mention skill development, role growth, and contribution to company."
                },
                {
                    "question": "Do you have any questions for us?",
                    "why_asked": "To check interest and engagement.",
                    "sample_answer": "Ask about team culture, projects, or growth opportunities."
                }
            ]
        
        return {"questions": questions}
    
    except Exception as e:
        # Return default questions on error
        return {"questions": [
            {
                "question": f"Tell me about yourself as a {request.role}.",
                "why_asked": "Standard opening question.",
                "sample_answer": "Brief introduction about your background."
            }
        ]}

@app.post("/generate-skill-roadmap")
async def generate_skill_roadmap(request: SkillRequest):
    try:
        prompt = SKILL_ROADMAP_PROMPT.format(
            role=request.role,
            experience=request.experience
        )
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a career coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        
        # Clean the content
        content = content.strip()
        content = re.sub(r'```', '', content)
        content = content.strip()
        
        # Ensure content is not empty or error message
        if not content or len(content) < 50 or "Error" in content:
            content = f"""
# {request.role} Skill Roadmap

## Core Skills (Must Learn)
1. Python Programming
2. Data Structures & Algorithms
3. Problem Solving

## Advanced Skills (Nice to Have)
1. Web Frameworks (Django/Flask)
2. Database Management
3. API Development

## Resources (Free Learning Links)
1. https://www.python.org/
2. https://www.w3schools.com/
3. https://www.freecodecamp.org/

## Timeline (Weeks to Master)
1. Core Skills: 4-6 weeks
2. Advanced Skills: 4-8 weeks
3. Projects: 2-4 weeks
            """
        
        return {"roadmap": content}
    
    except Exception as e:
        # Return default roadmap on error
        return {"roadmap": f"""
# {request.role} Skill Roadmap

## Core Skills (Must Learn)
1. Python Programming
2. Data Structures & Algorithms
3. Problem Solving

## Advanced Skills (Nice to Have)
1. Web Frameworks (Django/Flask)
2. Database Management
3. API Development

## Resources (Free Learning Links)
1. https://www.python.org/
2. https://www.w3schools.com/
3. https://www.freecodecamp.org/

## Timeline (Weeks to Master)
1. Core Skills: 4-6 weeks
2. Advanced Skills: 4-8 weeks
3. Projects: 2-4 weeks
        """}
# ================= HEALTH CHECK ================= #

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# ================= RUN ================= #

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)