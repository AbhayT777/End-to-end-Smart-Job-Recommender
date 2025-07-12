# testing the resume_extracter.py
from resume_parser.ocr_parser import extract_text_from_pdf
from resume_parser.resume_extracter import parse_resume

text = extract_text_from_pdf("data/sample_cv.pdf")
parsed_data = parse_resume(text)

print(parsed_data)
