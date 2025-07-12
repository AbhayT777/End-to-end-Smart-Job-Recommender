import re

def extract_contact_info(text):
    email = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone = re.findall(r"\+?\d[\d -]{8,12}\d", text)
    return {
        "email": email[0] if email else "",
        "phone": phone[0] if phone else ""
    }

def extract_skills(text, skill_list):
    found_skills = []
    text = text.lower()
    for skill in skill_list:
        if skill.lower() in text:
            found_skills.append(skill)
    return found_skills

def parse_resume(text):
    contact = extract_contact_info(text)
    skills = extract_skills(text, [
        'Python', 'Java', 'SQL', 'Machine Learning', 'Deep Learning',
        'Data Analysis', 'Django', 'Flask', 'AWS', 'Docker'
    ])
    return {
        "email": contact["email"],
        "phone": contact["phone"],
        "skills": skills
    }
