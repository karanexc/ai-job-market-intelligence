import spacy
from nlp.skill_dictionary import SKILLS

nlp = spacy.load("en_core_web_sm")

import spacy
from nlp.skill_dictionary import SKILLS

nlp = spacy.load("en_core_web_sm")


import re
from nlp.skill_dictionary import SKILLS


def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))