import os
import requests
from dotenv import load_dotenv
import streamlit as st
import re

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")


# -----------------------------
# Clean and prioritize skills
# -----------------------------
def clean_skill(skill):
    skill = skill.lower()
    skill = re.sub(r"[^a-zA-Z0-9\s]", "", skill)
    return skill.strip()


def prioritize_skills(skills):
    COMMON_SKILLS = [
        # Programming Languages
        "python",
        "java",
        "c++",
        "c#",
        "javascript",
        "typescript",
        "php",
        "r",
        "go",
        "scala",
        "sql",
        "html",
        "css",
        "bash",
        "kotlin",
        "swift",
        # Machine Learning / AI / Data Science
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "tensorflow",
        "pytorch",
        "keras",
        "nlp",
        "natural language processing",
        "computer vision",
        "transformers",
        "scikit-learn",
        "lightgbm",
        "xgboost",
        "opencv",
        "fastai",
        "huggingface",
        "bert",
        "llms",
        "mlflow",
        # Data Tools
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "power bi",
        "tableau",
        "data visualization",
        "feature engineering",
        "data analysis",
        # Cloud & DevOps
        "aws",
        "azure",
        "gcp",
        "cloud",
        "docker",
        "kubernetes",
        "terraform",
        "ci/cd",
        "github actions",
        "jenkins",
        "ansible",
        "devops",
        "cloud computing",
        "cloud engineer",
        "cloud security",
        # Frameworks & Libraries
        "django",
        "flask",
        "spring boot",
        "dotnet",
        ".net core",
        "react",
        "angular",
        "vue",
        "next.js",
        "express",
        "node.js",
        # Databases
        "mysql",
        "postgresql",
        "sql server",
        "mongodb",
        "redis",
        "oracle",
        "cosmos db",
        "bigquery",
        "firebase",
        # Tools / Platforms
        "jira",
        "git",
        "github",
        "bitbucket",
        "notion",
        "linux",
        "windows",
        "apache spark",
        "hadoop",
        "airflow",
        "etl",
        "data pipelines",
        # Testing
        "selenium",
        "testng",
        "cypress",
        "junit",
        "postman",
        "manual testing",
        "automation testing",
        # Misc
        "microservices",
        "api development",
        "rest apis",
        "graphql",
        "agile",
        "scrum",
        "product management",
        "system design",
        "software architecture",
    ]

    cleaned_skills = [clean_skill(s) for s in skills]
    prioritized = [s for s in cleaned_skills if s in COMMON_SKILLS]
    return prioritized  # top  relevant common skills


# -----------------------------
# Adzuna Job Fetcher
# -----------------------------
def get_adzuna_jobs(skills, location="in", max_results=10):
    if not skills:
        return []

    top_skills = prioritize_skills(skills)[
        :8
    ]  # Only top 5 relevant skills to avoid spammy queries

    if not top_skills:
        st.info("ℹ️ No common keywords found to query live job APIs.")
        return []

    # st.markdown("### 🌐 Real-Time Job Openings Based on Your Skills")

    all_jobs = []
    seen_urls = set()

    for skill in top_skills:
        query = skill
        url = f"https://api.adzuna.com/v1/api/jobs/{location}/search/1"
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": query,
            "results_per_page": max_results,
            "content-type": "application/json",
        }

        # 🐞 Debug info
        # st.write(f"🔍 Querying for: `{query}`")

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                st.warning(f"⚠️ Adzuna API error for '{query}': {response.status_code}")
                continue

            data = response.json()
            results = data.get("results", [])

            for job in results:
                job_url = job.get("redirect_url")
                if job_url and job_url not in seen_urls:
                    seen_urls.add(job_url)
                    all_jobs.append(
                        {
                            "title": job.get("title"),
                            "company": job.get("company", {}).get(
                                "display_name", "Unknown"
                            ),
                            "location": job.get("location", {}).get(
                                "display_name", "Unknown"
                            ),
                            "link": job_url,
                            "job_type": job.get("contract_time", "N/A"),
                        }
                    )

        except Exception as e:
            st.error(f"❌ Error fetching jobs for `{query}`: {e}")
            continue

    if not all_jobs:
        st.info("ℹ️ No live jobs currently found for your skillset. Try again later!")

    return all_jobs
