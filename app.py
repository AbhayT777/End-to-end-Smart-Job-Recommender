import streamlit as st
import os
import csv
import json
import hashlib
from dotenv import load_dotenv
from resume_parser.ocr_parser import extract_text_from_pdf, extract_text_from_image
from resume_parser.resume_extractor import parse_resume
from job_recommender.adzuna_jobs import get_adzuna_jobs

# ========================
# AUTHENTICATION FUNCTIONS
# ========================
USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password):
    users = load_users()
    return username in users and users[username]["password"] == hash_password(password)

def register_user(username, email, phone, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {
        "email": email,
        "phone": phone,
        "password": hash_password(password),
    }
    save_users(users)
    return True

# ========================
# SESSION SETUP
# ========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

# ========================
# HEADER AUTHENTICATION UI
# ========================
st.set_page_config(page_title="Skill Setu", layout="wide")
st.title("🤖 Skill Setu ")
st.markdown("<p style='font-size:16px; color:gray; margin-top:-15px;'>Bridge Your Skills to the Right Job.</p>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Log In"):
            st.session_state.auth_mode = "login"
    with col2:
        if st.button("🆕 Sign Up"):
            st.session_state.auth_mode = "signup"

# ========================
# SIGN UP FORM
# ========================
if st.session_state.auth_mode == "signup" and not st.session_state.logged_in:
    st.subheader("Create an Account")
    username = st.text_input("Username", key="signup_user")
    email = st.text_input("Email", key="signup_email")
    phone = st.text_input("Phone", key="signup_phone")
    password = st.text_input("Password", type="password", key="signup_pass")
    confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

    if st.button("Sign Up"):
        if not username or not email or not phone or not password:
            st.warning("Please fill all fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            if register_user(username, email, phone, password):
                st.success("Registration successful! You can now log in.")
                st.session_state.auth_mode = "login"
            else:
                st.error("Username already exists.")

# ========================
# LOGIN FORM
# ========================
elif st.session_state.auth_mode == "login" and not st.session_state.logged_in:
    st.subheader("Log In")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Log In"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid credentials.")

# ========================
# MAIN APP LOGIC
# ========================
if st.session_state.logged_in:
    st.markdown(f"✅ Logged in as **{st.session_state.username}**")
    if st.button("🚪 Log Out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.auth_mode = "login"
        st.stop()


    load_dotenv()

    st.markdown(
        """
        Upload your **CV (PDF or Image)** and get:
        - ✅ AI-based **skill extraction** from your CV  
        - 🌐 Real-time job openings based on your skills
        -    Please leave your valuable feedback to help us improve
        """
    )

    uploaded_file = st.file_uploader(
        "📄 Upload your Resume (PDF, JPG, PNG)", type=["pdf", "jpg", "jpeg", "png"]
    )

    if uploaded_file and "resume_processed" not in st.session_state:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        os.makedirs("data", exist_ok=True)
        save_path = os.path.join("data", "cv." + file_extension)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ Resume uploaded successfully!")

        with st.spinner("🔍 Extracting text from resume..."):
            text = (
                extract_text_from_pdf(save_path)
                if file_extension == "pdf"
                else extract_text_from_image(save_path)
            )

        with st.spinner("🧠 Extracting skills from your resume..."):
            parsed_data = parse_resume(text)
            st.session_state.extracted_skills = parsed_data.get("skills", [])

        if st.session_state.extracted_skills:
            st.session_state.resume_processed = True
        else:
            st.error("❌ No skills could be extracted from the CV.")

    if st.session_state.get("resume_processed"):
        st.markdown("### 🧩 Extracted Skills")
        st.write(", ".join(st.session_state.extracted_skills))

        country = st.selectbox(
            "🌍 Select Country",
            ["gb", "us", "in", "ca", "au"],
            index=2,
            key="country_select",
        )

        if "live_jobs" not in st.session_state or st.session_state.get("last_country") != country:
            with st.spinner("🌐 Fetching real-time jobs..."):
                st.session_state.live_jobs = get_adzuna_jobs(
                    st.session_state.extracted_skills, location=country
                )
                st.session_state.job_page = 1
                st.session_state.last_country = country

        live_jobs = st.session_state.live_jobs

        if live_jobs:
            st.markdown("### 📌 Here are the recommended Jobs for You ")
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
                selected_page = st.selectbox(
                    "📄 Go to Page",
                    page_numbers,
                    index=st.session_state.job_page - 1,
                    key="job_pagination",
                )
                st.session_state.job_page = int(selected_page)

            start_idx = (st.session_state.job_page - 1) * jobs_per_page
            end_idx = start_idx + jobs_per_page
            current_jobs = live_jobs[start_idx:end_idx]

            for job in current_jobs:
                with st.container():
                    st.markdown(
                        f"**🔹 {job['title']}** at `{job['company']}` — *{job['location']}*"
                    )
                    st.markdown(f"🔗 [Apply here]({job['link']})")
                    st.markdown("---")
        else:
            st.info("ℹ️ No live jobs currently found for your skillset. Try again later!")

    # ========================
    # FEEDBACK SECTION
    # ========================
    st.markdown("## 💬 We'd love your feedback!")

    name = st.text_input("👤 Your Name")
    email = st.text_input("📧 Your Email")
    phone = st.text_input("📱 Contact Number")
    feedback = st.text_area("✍️ Your Feedback")

    if st.button("✅ Submit Feedback"):
        if name and email and feedback:
            os.makedirs("data", exist_ok=True)
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

    # ========================
    # FOOTER
    # ========================
    st.markdown("---")
    st.markdown("### 🙋‍♂️ About This App")
    st.markdown(
        """
        **Smart Job Recommender** is an AI-based platform that extracts skills from your uploaded resume and recommends real-time job openings.

        👨‍💻 **Developed by:** [Abhay Kumar Tiwari (LinkedIN profile)](https://www.linkedin.com/in/abhay-kumar-tiwari-0191a6121/)  
        📧 Email: tabhay373@gmail.com  
        🔗 GitHub: [github.com/AbhayT777](https://github.com/AbhayT777)
        """
    )
