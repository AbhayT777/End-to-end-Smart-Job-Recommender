import streamlit as st
from resume_parser.ocr_parser import extract_text_from_pdf, extract_text_from_image
from resume_parser.resume_extractor import parse_resume
from job_recommender.job_matcher import load_jobs, match_jobs_with_suggestions
import os

st.set_page_config(page_title="Smart Job Recommender", layout="wide")
st.title(" Smart Job Recommender from CV")

st.markdown("""
Upload your **CV (PDF or image)** and get **matching jobs** with **skills suggestions** to improve your profile.  
""")

# File uploader
uploaded_file = st.file_uploader("Upload your Resume (PDF, JPG, PNG)", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()

    # Save the uploaded file to 'data/' folder
    save_path = os.path.join("data", "cv." + file_extension)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(" Resume uploaded successfully!")

    # Extract text
    with st.spinner(" Extracting text from resume..."):
        if file_extension == "pdf":
            text = extract_text_from_pdf(save_path)
        else:
            text = extract_text_from_image(save_path)

    # Parse the resume
    with st.spinner(" Parsing resume and extracting skills..."):
        parsed_data = parse_resume(text)
        extracted_skills = parsed_data.get("skills", [])

    if extracted_skills:
        st.markdown("###  Extracted Skills")
        st.write(", ".join(extracted_skills))

        # Load jobs and recommend
        with st.spinner(" Finding matching jobs..."):
            jobs = load_jobs()
            recommendations = match_jobs_with_suggestions(extracted_skills, jobs)

        if recommendations:
            st.markdown("###  Recommended Jobs for You")
            for job in recommendations:
                with st.container():
                    st.markdown(f"** {job['title']}** at `{job['company']}` — *{job['location']}*")
                    st.markdown(f" [Apply here]({job['link']})")
                    st.markdown(f" **Matched Skills:** {', '.join(job['matched_skills'])}")
                    st.markdown(f" **Suggested Skills to Learn:** {', '.join(job['suggested_skills']) if job['suggested_skills'] else 'None'}")
                    st.markdown("---")
        else:
            st.warning(" Sorry, no strongly matching jobs found. Try improving your skillset.")
    else:
        st.error(" No skills were extracted from the CV.")
