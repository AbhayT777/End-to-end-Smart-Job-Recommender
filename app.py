import streamlit as st
import os
import csv
from dotenv import load_dotenv
from resume_parser.ocr_parser import extract_text_from_pdf, extract_text_from_image
from resume_parser.resume_extractor import parse_resume
from job_recommender.adzuna_jobs import get_adzuna_jobs

load_dotenv()

st.set_page_config(page_title="Smart Job Recommender", layout="wide")
st.title("🤖 Smart Job Recommender from CV")

st.markdown("""
Upload your **CV (PDF or Image)** and get:
- ✅ AI-based **skill extraction** from your CV
- 🌐 Real-time job openings based on your skills (via Adzuna)
- 💬 Leave feedback to help us improve
""")

uploaded_file = st.file_uploader("📄 Upload your Resume (PDF, JPG, PNG)", type=["pdf", "jpg", "jpeg", "png"])

# ----------------------------
# Resume Upload and Processing
# ----------------------------
if uploaded_file and "resume_processed" not in st.session_state:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    save_path = os.path.join("data", "cv." + file_extension)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("✅ Resume uploaded successfully!")

    # OCR & Skill Extraction
    with st.spinner("🔍 Extracting text from resume..."):
        if file_extension == "pdf":
            text = extract_text_from_pdf(save_path)
        else:
            text = extract_text_from_image(save_path)

    with st.spinner("🧠 Extracting skills from your resume..."):
        parsed_data = parse_resume(text)
        st.session_state.extracted_skills = parsed_data.get("skills", [])

    if st.session_state.extracted_skills:
        st.session_state.resume_processed = True
    else:
        st.error("❌ No skills could be extracted from the CV.")

# ----------------------------
# Job Search and Display
# ----------------------------
if st.session_state.get("resume_processed"):
    st.markdown("### 🧩 Extracted Skills")
    st.write(", ".join(st.session_state.extracted_skills))

    country = st.selectbox("🌍 Select Country", ["gb", "us", "in", "ca", "au"], index=2, key="country_select")

    if "live_jobs" not in st.session_state or st.session_state.get("last_country") != country:
        with st.spinner("🌐 Fetching real-time jobs..."):
            st.session_state.live_jobs = get_adzuna_jobs(st.session_state.extracted_skills, location=country)
            st.session_state.job_page = 1
            st.session_state.last_country = country

    live_jobs = st.session_state.live_jobs

    if live_jobs:
        st.markdown("### 📌 Recommended Jobs for You")

        jobs_per_page = 5
        total_jobs = len(live_jobs)
        total_pages = (total_jobs - 1) // jobs_per_page + 1

        if "job_page" not in st.session_state:
            st.session_state.job_page = 1

        col1, col2, col3 = st.columns([1, 6, 1])
        with col1:
            if st.session_state.job_page > 1:
                if st.button("⬅️ Prev"):
                    st.session_state.job_page -= 1

        with col3:
            if st.session_state.job_page < total_pages:
                if st.button("Next ➡️"):
                    st.session_state.job_page += 1

        with col2:
            page_numbers = [str(i) for i in range(1, total_pages + 1)]
            selected_page = st.selectbox("📄 Go to Page", page_numbers, index=st.session_state.job_page - 1, key="job_pagination")
            st.session_state.job_page = int(selected_page)

        start_idx = (st.session_state.job_page - 1) * jobs_per_page
        end_idx = start_idx + jobs_per_page
        current_jobs = live_jobs[start_idx:end_idx]

        for job in current_jobs:
            with st.container():
                st.markdown(f"**🔹 {job['title']}** at `{job['company']}` — *{job['location']}*")
                st.markdown(f"🔗 [Apply here]({job['link']})")
                st.markdown("---")
    else:
        st.info("ℹ️ No live jobs currently found for your skillset. Try again later!")

# ----------------------------
# Feedback Section
# ----------------------------
st.markdown("## 💬 We'd love your feedback!")

name = st.text_input("👤 Your Name")
email = st.text_input("📧 Your Email")
phone = st.text_input("📱 Contact Number")
feedback = st.text_area("✍️ Your Feedback")

if st.button("✅ Submit Feedback"):
    if name and email and feedback:
        feedback_file = "data/user_feedback.csv"
        file_exists = os.path.isfile(feedback_file)

        with open(feedback_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Name", "Email", "Phone", "Feedback"])
            writer.writerow([name, email, phone, feedback])
        st.success("🙏 Thanks for your feedback!")
    else:
        st.error("⚠️ Please fill in your name, email, and feedback.")


# -------------------
# 📌 App Info Footer
# -------------------
st.markdown("---")
st.markdown("### 🙋‍♂️ About This App")
st.markdown("""
**Smart Job Recommender** is an AI-based platform that extracts skills from your uploaded resume and recommends real-time job openings using Adzuna Jobs API.

👨‍💻 **Developed & Owned by:** [Abhay Kumar Tiwari](https://www.linkedin.com/in/abhay-kumar-tiwari-0191a6121/)  
📧 Email: tabhay373@gmail.com  
🔗 GitHub: [github.com/AbhayT777](https://github.com/AbhayT777)

Feel free to share, contribute, or reach out if you're hiring! 🚀
""")

#ci check 