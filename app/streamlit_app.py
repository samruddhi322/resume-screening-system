import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st
import matplotlib.pyplot as plt

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


st.set_page_config(
    page_title="Resume Screening System",
    page_icon="📄",
    layout="wide"
)


st.markdown(
    """
    <style>

    /* WHOLE APP */
    .stApp {
        background-color: #f7efe5;
        color: #4b3832;
    }

    /* REMOVE TOP BLACK HEADER */
    header[data-testid="stHeader"] {
        background-color: #f7efe5 !important;
    }

    /* REMOVE TOOLBAR BLACK AREA */
    div[data-testid="stToolbar"] {
        background-color: #f7efe5 !important;
    }


    /* MAIN CONTAINER */
    .main {
        padding-top: 2rem;
        background-color: #f7efe5;
    }

    /* SIDEBAR MAIN */
section[data-testid="stSidebar"] {
    background-color: #5c4033 !important;
    border-right: 1px solid #dbc1ac;
}

/* REMOVE STREAMLIT DEFAULT BLUE */
section[data-testid="stSidebar"] div[data-testid="stSidebarContent"] {
    background-color: #efe1d1 !important;
}

/* STYLE THE INFO CARD */
section[data-testid="stSidebar"] div[data-baseweb="notification"] {
    background-color: #f3e5d7 !important;
    border: 1px solid #dbc1ac !important;
    border-radius: 20px !important;
    padding: 18px !important;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05) !important;
}

/* TEXT COLORS */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] div {
    color: #5c4033 !important;
}

    /* HEADINGS */
    h1, h2, h3 {
        color: #7f5539;
        font-family: 'Segoe UI', sans-serif;
    }

    /* NORMAL TEXT */
    p, label, div {
        color: #5c4033;
        font-family: 'Segoe UI', sans-serif;
    }

    /* METRIC CARDS */
    .stMetric {
        background-color: #fff8f0;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #e6ccb2;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }

    /* FILE UPLOADER OUTER BOX */
    .stFileUploader {
        background-color: #fff8f0 !important;
        padding: 18px;
        border-radius: 18px;
        border: 1px solid #e6ccb2 !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }

    /* FILE UPLOADER INNER DROPZONE */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #fff8f0 !important;
        border: 1px solid #e6ccb2 !important;
        border-radius: 18px !important;
    }

    /* REMOVE BLACK INSIDE AREA */
    [data-testid="stFileUploaderDropzone"] div {
        background-color: transparent !important;
        color: #5c4033 !important;
    }

    /* UPLOAD BUTTON */
    .stFileUploader button {
        background: linear-gradient(
            135deg,
            #ddb892,
            #b08968
        ) !important;

        color: white !important;

        border-radius: 12px !important;

        border: none !important;

        font-weight: 600 !important;
    }

/* TEXT AREA CONTAINER */
[data-baseweb="textarea"] {

    border-radius: 15px !important;

    border: 1px solid #b08968 !important;

    background-color: #fff8f0 !important;

    box-shadow: none !important;
}

/* INNER TEXTAREA */
[data-baseweb="textarea"] textarea {

    background-color: #fff8f0 !important;

    color: #5c4033 !important;

    border: none !important;

    outline: none !important;

    box-shadow: none !important;

    font-size: 15px !important;

    padding: 12px !important;
}

/* REMOVE RED/ORANGE FOCUS BORDER */
[data-baseweb="textarea"]:focus-within {

    border: 1px solid #b08968 !important;

    box-shadow: 0 0 0 1px #b08968 !important;

    outline: none !important;
}

    /* BUTTON */
    div.stButton > button {

        background: linear-gradient(
            135deg,
            #ddb892,
            #b08968
        );

        color: white;

        border-radius: 14px;

        height: 3.3em;

        font-size: 18px;

        font-weight: 600;

        border: none;

        width: 100%;

        transition: all 0.3s ease;

        box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    }

    /* BUTTON HOVER */
    div.stButton > button:hover {

        background: linear-gradient(
            135deg,
            #e6ccb2,
            #c6a27e
        );

        transform: translateY(-2px);

        box-shadow: 0px 6px 14px rgba(0,0,0,0.12);
    }

    /* ALERT BOXES */
    div[data-testid="stAlert"] {

        border-radius: 15px;

        background-color: #fff8f0;

        color: #5c4033;
    }

    /* PROGRESS BAR */
    .stProgress > div > div > div > div {
        background-color: #b08968;
    }

    /* DIVIDERS */
    hr {
        border-color: #dbc1ac;
    }

    /* SKILL TAGS */
    .skill-box {
        background-color: #ffe8d6;
        padding: 8px 14px;
        border-radius: 12px;
        display: inline-block;
        margin: 5px;
        color: #7f5539;
        font-size: 14px;
    }

    /* FORCE SIDEBAR ARROW SVG COLOR */
button[kind="header"] svg {
    fill: #7f5539 !important;
}

    /* REMOVE FILE SIZE TEXT */
[data-testid="stFileUploader"] small {
    display: none !important;
}

/* SIDEBAR COLLAPSE BUTTON */
button[kind="header"] {

    color: #7f5539 !important;

    background-color: transparent !important;
}

/* HOVER EFFECT */
button[kind="header"]:hover {

    background-color: #efe1d1 !important;

    border-radius: 10px;
}

/* REMOVE SIDEBAR DIVIDER LINE */
section[data-testid="stSidebar"] hr {
    display: none !important;
}

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    #  Intelligent Resume Screening System
    
    Match resumes with job descriptions using:
    
    - NLP Preprocessing
    - TF-IDF Vectorization
    - Cosine Similarity
    - Skill Gap Analysis
    """
)


st.sidebar.title(" About")

st.sidebar.info(
    """
    This system analyzes resumes using:
    
     TF-IDF Vectorization  
     Cosine Similarity  
     Skill Extraction  
     NLP Preprocessing  
    
    ---
    
   
    
    - Python
    - Streamlit
    - Scikit-learn
    - NLTK
    - Matplotlib
    """
)


col1, col2 = st.columns(2)

with col1:

    uploaded_file = st.file_uploader(
        " Upload Resume PDF",
        type=["pdf"]
    )

with col2:

    job_description = st.text_area(
        " Paste Job Description",
        height=250
    )


analyze_button = st.button(
    " Analyze Resume",
    use_container_width=True
)


if analyze_button and uploaded_file and job_description:

    with st.spinner("Analyzing Resume..."):


        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.read())

        resume_text = extract_text_from_pdf(
            "temp_resume.pdf"
        )

        resume_text = clean_text(resume_text)

        resume_text = remove_stopwords(resume_text)

        job_text = clean_text(job_description)

        job_text = remove_stopwords(job_text)

        match_score = calculate_similarity(
            resume_text,
            job_text
        )

        resume_skills = extract_skills(resume_text)

        job_skills = extract_skills(job_text)

        missing_skills = get_missing_skills(
            resume_skills,
            job_skills
        )


        matched_skills = len(
            set(resume_skills).intersection(set(job_skills))
        )

        missing_count = len(missing_skills)

        skill_match_score = (
            matched_skills / len(job_skills)
        ) * 100 if job_skills else 0

        st.divider()

        st.header(" Analysis Results")

        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:

            st.subheader("TF-IDF Match Score")

            st.metric(
                label="Resume Similarity",
                value=f"{match_score}%"
            )

            st.progress(min(int(match_score), 100))

        with metric_col2:

            st.subheader("Skill Match Score")

            st.metric(
                label="Skill Overlap",
                value=f"{round(skill_match_score, 2)}%"
            )

            st.progress(min(int(skill_match_score), 100))

        st.divider()


        skill_col1, skill_col2 = st.columns(2)

        with skill_col1:

            st.subheader(" Extracted Resume Skills")

            if resume_skills:

                for skill in resume_skills:
                    st.markdown(f"-  {skill}")

            else:
                st.warning("No skills detected.")

        with skill_col2:

            st.subheader(" Missing Skills")

            if missing_skills:

                for skill in missing_skills:
                    st.markdown(f"-  {skill}")

            else:
                st.success("No missing skills detected!")

        st.divider()


        st.subheader(" Skill Match Visualization")

        fig, ax = plt.subplots(figsize=(5, 5))

        labels = [
            "Matched Skills",
            "Missing Skills"
        ]

        sizes = [
            matched_skills,
            missing_count
        ]

        ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%'
        )

        st.pyplot(fig)


        st.divider()

        st.subheader(" Final Recommendation")

        if match_score >= 75:

            st.success(
                "Excellent match for this role."
            )

        elif match_score >= 50:

            st.warning(
                "Moderate match. Consider improving missing skills."
            )

        else:

            st.error(
                "Low match score. Resume needs improvement for this role."
            )