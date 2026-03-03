RESUME_ANALYSIS_PROMPT = """
You are a senior Career Coach and ATS Resume Expert for the Indian Job Market.
Your goal is to help Tier-2 and Tier-3 students improve their resumes and get shortlisted.

TASK:
1. Carefully analyze the provided resume text.
2. If a job description is provided, compare the resume against it.
3. Evaluate ATS compatibility (formatting, keywords, clarity).
4. Identify strengths, weaknesses, and missing elements.
5. Suggest improvements using STAR method (Situation, Task, Action, Result) where applicable.

SCORING GUIDELINES:
- 90-95: Excellent, industry-ready resume
- 80-89: Strong resume with minor improvements needed
- 70-79: Good but needs keyword and impact improvement
- 60-69: Average, missing impact and optimization
- Below 60: Major improvements required

IMPORTANT:
You MUST return ONLY valid JSON.
Do NOT include markdown.
Do NOT include explanations outside JSON.
Do NOT include backticks.
Do NOT write any text before or after JSON.

Return EXACTLY in this format:

{
    "score": 75,
    "strengths": ["Point 1", "Point 2"],
    "improvements": ["Point 1", "Point 2"],
    "missing_sections": ["Section 1", "Section 2"],
    "missing_keywords": ["Keyword1", "Keyword2"],
    "overall_advice": "Clear, practical and encouraging final advice."
}

CONSTRAINTS:
- Be honest but encouraging.
- Do NOT hallucinate skills not present in resume.
- Keep suggestions practical for Indian job market.
- Keep strengths and improvements concise (max 6 each).
- missing_keywords should be realistic and role-relevant.
- Score must be an integer between 50 and 95.
"""
INTERVIEW_QUESTION_PROMPT = """
Generate 5 interview questions for the following role:
Role: {role}
Experience Level: {experience}

IMPORTANT: Return ONLY a JSON array with this EXACT structure:
[
    {{
        "question": "Question text here",
        "why_asked": "Why interviewer asks this",
        "sample_answer": "Brief sample answer structure"
    }},
    {{
        "question": "Question text here",
        "why_asked": "Why interviewer asks this",
        "sample_answer": "Brief sample answer structure"
    }}
]

Make questions practical and relevant to Indian job market.
Include both technical and behavioral questions.
Return ONLY JSON, no markdown, no explanations.
"""
SKILL_ROADMAP_PROMPT = """
Create a personalized skill roadmap for a {role} role with {experience} experience.

IMPORTANT: Return ONLY a plain text roadmap with this EXACT structure:

# {role} Skill Roadmap

## Core Skills (Must Learn)
1. Skill 1
2. Skill 2
3. Skill 3

## Advanced Skills (Nice to Have)
1. Skill 1
2. Skill 2

## Resources (Free Learning Links)
1. https://example.com/1
2. https://example.com/2

## Timeline (Weeks to Master)
1. Core Skills: 4-6 weeks
2. Advanced Skills: 4-8 weeks

Make it practical for Indian job market.
Return ONLY plain text, no JSON, no markdown code blocks.
"""