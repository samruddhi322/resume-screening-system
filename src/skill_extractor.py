SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "mysql",
    "mongodb",
    "aws",
    "docker",
    "kubernetes",
    "tensorflow",
    "pytorch",
    "machine learning",
    "deep learning",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "fastapi",
    "streamlit",
    "git",
    "github",
    "linux"
]

def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in SKILLS:

        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills

def get_missing_skills(resume_skills, job_skills):

    missing = []

    for skill in job_skills:

        if skill not in resume_skills:
            missing.append(skill)

    return missing