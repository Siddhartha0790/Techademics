# ai_engine/ollama_utils.py

import ollama

def extract_skills_from_profile(profile_data: str) -> list[str]:
    prompt = f"""
You are a skill extraction assistant. Extract a clean list of hard and soft skills, technologies, and tools from this profile:

{profile_data}

Return only a comma-separated list of skills.
"""
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]
    skills = [skill.strip() for skill in content.split(",") if skill.strip()]
    return skills


def match_jobs_to_skills(skills: list[str], jobs: list[dict]) -> list[dict]:
    skill_str = ", ".join(skills)
    job_block = "\n\n".join([
        f"[{i+1}] Title: {job['title']}\nDescription: {job['description']}"
        for i, job in enumerate(jobs)
    ])

    prompt = f"""
You are a job recommendation assistant.

Given the following user's skills:
{skill_str}

And the following job descriptions:
{job_block}

Select the top 5 most relevant jobs for the user based on skills match.
Return them in this format:
[
  {{ "index": 1, "reason": "Matches Python and SQL" }},
  {{ "index": 4, "reason": "Strong match with data analysis and visualization" }},
  ...
]
Only return the list.
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    content = response["message"]["content"]
    try:
        return json.loads(content)
    except:
        return []


import json

def match_live_jobs(skills: list[str], jobs: list[dict]) -> list[dict]:
    skill_str = ", ".join(skills)
    job_block = "\n\n".join([
        f"[{i+1}] Title: {job['title']}\nDescription: {job['description']}"
        for i, job in enumerate(jobs)
    ])

    prompt = f"""
You are an AI job matching assistant.

The user has these skills:
{skill_str}

Here are live job openings:
{job_block}

Pick the top 5 most relevant jobs.
Return this format:
[
  {{ "index": 3, "reason": "Strong match with backend Python skills" }},
  ...
]
Only return the JSON list.
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return json.loads(response["message"]["content"])
    except:
        return []