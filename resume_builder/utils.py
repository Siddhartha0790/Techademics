import google.generativeai as genai
from django.conf import settings
import json


def enhance_with_ollama(prompt_text: str) -> str:
    """
    Enhances a given text using Gemini (Google Generative AI).
    Used for quick single-field enhancement.
    """
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(settings.GEMINI_MODEL)

    system_prompt = (
        "You are a professional technical writer. "
        "Enhance the following content to make it clear, impressive, and resume-worthy. "
        "Focus on strong action verbs, real-world impact, technologies used, and clean formatting. "
        "Don't invent anything new, just polish what's already there. "
        "Return the enhanced description in bullet points. "
        "Limit to 3 bullet points."
    )

    full_prompt = f"{system_prompt}\n\n{prompt_text}"
    response = model.generate_content(full_prompt)
    return response.text


def generate_full_resume(profile, email):
    """
    Uses Gemini AI to generate a complete, detailed, professional resume
    from the user's profile data. Returns structured dict with all sections
    enhanced and formatted for a real resume.
    """
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(settings.GEMINI_MODEL)

    prompt = f"""You are an expert resume writer with 15+ years of experience crafting ATS-optimized, 
professional resumes. Generate a complete, polished, professional resume based on the following profile data.

PROFILE DATA:
- Name: {profile.full_name}
- Email: {email}
- Phone: {profile.phone_number}
- Location: {profile.location}
- Skills: {profile.skills}
- Education: {profile.education}
- Experience: {profile.experience}
- Projects: {profile.projects}
- Achievements: {profile.achievements}

INSTRUCTIONS:
1. Write a compelling 2-3 sentence professional summary highlighting their strongest qualifications.
2. Format skills into categorized groups (e.g., "Languages", "Frameworks", "Tools", "Soft Skills") — return as a single string with categories separated by " | ".
3. Rewrite education with proper formatting — include degree, institution, dates if available.
4. Rewrite experience with strong action verbs, quantified achievements where possible. Each role should have a title, company/context, and 2-3 bullet points.
5. Enhance project descriptions with technologies used, your role, and impact. Each project: name, tech stack, and 2-3 bullet points.
6. Polish achievements to sound impressive and professional.

IMPORTANT: 
- Do NOT invent new information. Only enhance and restructure what is provided.
- If a field is empty or says "Not provided", return an empty string for it.
- Return ONLY valid JSON, no markdown fences, no commentary.

Return this exact JSON structure:
{{
  "summary": "Professional summary text...",
  "skills": "Languages: Python, Java | Frameworks: Django, React | Tools: Git, Docker",
  "education": "Enhanced education text with proper formatting...",
  "experience": "Enhanced experience with bullet points...",
  "projects": "Enhanced projects with tech stack and impact...",
  "achievements": "Enhanced achievements..."
}}
"""

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Strip markdown code fences if present
        if raw.startswith('```'):
            raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()

        result = json.loads(raw)
        return {
            'summary': result.get('summary', ''),
            'skills': result.get('skills', profile.skills),
            'education': result.get('education', profile.education),
            'experience': result.get('experience', profile.experience),
            'projects': result.get('projects', profile.projects),
            'achievements': result.get('achievements', profile.achievements),
        }
    except Exception:
        # Fallback: return original profile data unenhanced
        return {
            'summary': '',
            'skills': profile.skills,
            'education': profile.education,
            'experience': profile.experience,
            'projects': profile.projects,
            'achievements': profile.achievements,
        }