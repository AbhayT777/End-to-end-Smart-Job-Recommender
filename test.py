# testing the resume_extracter.py--------------------------------------------
# from resume_parser.ocr_parser import extract_text_from_pdf
# from resume_parser.resume_extracter import parse_resume

# text = extract_text_from_pdf("data/sample_cv.pdf")
# parsed_data = parse_resume(text)

# print(parsed_data)





# tesing the job_matcher.py---------------------------------------------------
from resume_parser.ocr_parser import extract_text_from_pdf
from resume_parser.resume_extractor import parse_resume
from job_recommender.job_matcher import load_jobs, match_jobs_with_suggestions

# Step 1: Extract text from uploaded CV
cv_path = "data/sample_cv.pdf"
text = extract_text_from_pdf(cv_path)

# Step 2: Parse resume to extract skills
parsed_data = parse_resume(text)
extracted_skills = parsed_data.get("skills", [])

# Step 3: Load job listings
jobs = load_jobs()

# Step 4: Get recommendations
recommendations = match_jobs_with_suggestions(extracted_skills, jobs)

# Step 5: Display results
print("\n Extracted Skills from Resume:")
print(", ".join(extracted_skills))

print("\n Recommended Jobs and Suggested Skills:\n")

for job in recommendations:
    print(f"{job['title']} at {job['company']} ({job['location']})")
    print(f" Matched Skills: {', '.join(job['matched_skills'])}")
    print(f" Suggested Skills to Learn: {', '.join(job['suggested_skills'])}")
    print(f" Apply: {job['link']}\n")



