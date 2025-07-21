import re
import spacy
from fuzzywuzzy import fuzz

nlp = spacy.load("en_core_web_sm", disable=["ner"])  # Disable unused components for speed

def load_skill_library(filepath="data/skills_library.txt"):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def extract_contact_info(text):
    email = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone = re.findall(r"\+?\d[\d -]{8,12}\d", text)
    return {"email": email[0] if email else "", "phone": phone[0] if phone else ""}


def extract_skills(text, skill_library):
    doc = nlp(text.lower())
    found_skills = set()

    # Use set comprehension for faster lookup
    cv_words = {token.text.strip() for token in doc if token.is_alpha and not token.is_stop}
    cv_phrases = {chunk.text.strip().lower() for chunk in doc.noun_chunks}

    for skill in skill_library:
        skill_lower = skill.lower()

        if any(fuzz.token_sort_ratio(skill_lower, phrase) >= 90 for phrase in cv_phrases):
            found_skills.add(skill)
            continue

        if any(fuzz.ratio(skill_lower, word) >= 90 for word in cv_words):
            found_skills.add(skill)

    return list(found_skills)


def parse_resume(text):
    contact = extract_contact_info(text)
    skill_library = load_skill_library()
    skills = extract_skills(text, skill_library)
    return {"email": contact["email"], "phone": contact["phone"], "skills": skills}
