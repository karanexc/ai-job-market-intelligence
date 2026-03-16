import spacy
from nlp.skill_dictionary import SKILLS

nlp = spacy.load("en_core_web_sm")

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))