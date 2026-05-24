import sys
import os
import shutil

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from src.preprocessing import (
    extract_text_from_pdf,
    clean_text,
    remove_stopwords
)

from src.matcher import calculate_similarity

from src.skill_extractor import (
    extract_skills,
    get_missing_skills
)

app = FastAPI(
    title="Resume Screening API",
    description="NLP-powered Resume Screening System API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():

    return {
        "message": "Resume Screening API is Running Successfully "
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }

@app.post("/score_resume")
async def score_resume(

    resume: UploadFile = File(...),

    job_description: str = Form(...)

):

    try:

        if not resume.filename.endswith(".pdf"):

            return {
                "error": "Only PDF files are allowed."
            }

        temp_file_path = "temp_resume.pdf"

        with open(temp_file_path, "wb") as buffer:

            shutil.copyfileobj(
                resume.file,
                buffer
            )

        resume_text = extract_text_from_pdf(
            temp_file_path
        )

        resume_text = clean_text(
            resume_text
        )

        resume_text = remove_stopwords(
            resume_text
        )

        job_text = clean_text(
            job_description
        )

        job_text = remove_stopwords(
            job_text
        )

        match_score = calculate_similarity(
            resume_text,
            job_text
        )

        resume_skills = extract_skills(
            resume_text
        )

        job_skills = extract_skills(
            job_text
        )

        missing_skills = get_missing_skills(
            resume_skills,
            job_skills
        )

        matched_skills = len(
            set(resume_skills).intersection(
                set(job_skills)
            )
        )

        skill_match_score = (
            matched_skills / len(job_skills)
        ) * 100 if job_skills else 0

        if match_score >= 75:

            recommendation = (
                "Excellent match for this role."
            )

        elif match_score >= 50:

            recommendation = (
                "Moderate match. Consider improving missing skills."
            )

        else:

            recommendation = (
                "Low match score. Resume needs improvement for this role."
            )

        return {

            "success": True,

            "match_score": round(
                match_score,
                2
            ),

            "skill_match_score": round(
                skill_match_score,
                2
            ),

            "resume_skills": resume_skills,

            "job_skills": job_skills,

            "missing_skills": missing_skills,

            "recommendation": recommendation
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

@app.post("/extract_skills")
async def extract_resume_skills(

    resume: UploadFile = File(...)

):

    try:

        if not resume.filename.endswith(".pdf"):

            return {
                "error": "Only PDF files are allowed."
            }

        temp_file_path = "temp_resume.pdf"

        with open(temp_file_path, "wb") as buffer:

            shutil.copyfileobj(
                resume.file,
                buffer
            )

        resume_text = extract_text_from_pdf(
            temp_file_path
        )

        resume_text = clean_text(
            resume_text
        )

        resume_text = remove_stopwords(
            resume_text
        )

        skills = extract_skills(
            resume_text
        )

        return {

            "success": True,

            "skills": skills
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }