import json

def load_jobs(filepath="data/jobs.json"):
    with open(filepath, "r") as f:
        return json.load(f)

def match_jobs_with_suggestions(user_skills, jobs):
    recommendations = []

    for job in jobs:
        job_skills = job.get("skills", [])
        matched = list(set(user_skills) & set(job_skills))
        missing = list(set(job_skills) - set(user_skills))
        match_score = len(matched)

        # Only include if matched_skills > suggested_skills
        if match_score > 0 and match_score > len(missing):
            job_info = {
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "link": job["link"],
                "match_score": match_score,
                "matched_skills": matched,
                "suggested_skills": missing
            }
            recommendations.append(job_info)

    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations[:5]
