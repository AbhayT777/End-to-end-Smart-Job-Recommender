import json

def load_jobs(filepath="data/jobs.json"):
    with open(filepath, "r") as f:
        return json.load(f)

def match_jobs_with_suggestions(user_skills, jobs, threshold=0.4):
    recommendations = []

    # Normalize user skills
    user_skills = [s.lower().strip() for s in user_skills]

    for job in jobs:
        job_skills = [s.lower().strip() for s in job.get("skills", [])]
        matched = list(set(user_skills) & set(job_skills))
        missing = list(set(job_skills) - set(user_skills))

        if not job_skills:
            continue  # Skip if job has no skills listed

        match_ratio = len(matched) / len(job_skills)

        if match_ratio >= threshold and len(matched) > 0:
            recommendations.append({
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "link": job["link"],
                "match_score": round(match_ratio * 100, 1),  # percentage
                "matched_skills": matched,
                "suggested_skills": missing
            })

    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations
