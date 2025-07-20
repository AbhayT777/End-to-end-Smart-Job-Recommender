# import requests

# def get_live_jobs_from_remotive(user_skills, max_jobs=5):
#     keywords = "+".join(user_skills[:5])  # use top 5 skills
#     url = f"https://remotive.io/api/remote-jobs?search={keywords}"

#     response = requests.get(url)
#     if response.status_code != 200:
#         return []

#     jobs = response.json().get("jobs", [])
#     live_jobs = []

#     for job in jobs[:max_jobs]:
#         live_jobs.append({
#             "title": job["title"],
#             "company": job["company_name"],
#             "location": job["candidate_required_location"],
#             "link": job["url"],
#             "job_type": job["job_type"]
#         })

#     return live_jobs

import requests

COMMON_SKILLS = [
    "python",
    "sql",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "tensorflow",
    "pytorch",
    "javascript",
    "html",
    "css",
    "java",
    "c++",
    "c#",
    "flask",
    "django",
    "git",
    "pandas",
    "numpy",
    "react",
    "linux",
    "postgresql",
    "mongodb",
    "machine learning",
]


def get_live_jobs_from_remotive(user_skills, max_jobs=5):
    # Filter user_skills to only common broad ones
    normalized = [s.lower().strip() for s in user_skills]
    relevant = [s for s in normalized if s in COMMON_SKILLS]

    # fallback: default skills if none match
    if not relevant:
        relevant = ["python", "sql", "aws"]

    # only keep top 3 for the search query
    query = "+".join(relevant[:3])
    url = f"https://remotive.io/api/remote-jobs?search={query}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return []

        jobs = response.json().get("jobs", [])
        results = []

        for job in jobs[:max_jobs]:
            results.append(
                {
                    "title": job["title"],
                    "company": job["company_name"],
                    "location": job["candidate_required_location"],
                    "link": job["url"],
                    "job_type": job["job_type"],
                }
            )

        return results

    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return []
