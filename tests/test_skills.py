from src.skill_extractor import (
    extract_skills,
    get_missing_skills
)

resume_text = """
Experienced Python developer with SQL and AWS.
"""

job_description = """
Looking for Python, SQL, Docker,
AWS, and machine learning experience.
"""

resume_skills = extract_skills(resume_text)

job_skills = extract_skills(job_description)

missing_skills = get_missing_skills(
    resume_skills,
    job_skills
)

print("Resume Skills:", resume_skills)
print("Job Skills:", job_skills)
print("Missing Skills:", missing_skills)