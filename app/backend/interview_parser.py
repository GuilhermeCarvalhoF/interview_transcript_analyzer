#########
## imports
#########

import re
import spacy


###########
## spacy model
###########
nlp = spacy.load("en_core_web_sm")

############
## keywords
############

skills_keywords = [
    "communication", "leadership", "problem-solving", "teamwork", "adaptability",
    "creativity", "collaboration", "time management", "critical thinking", "initiative",
    "analytical thinking", "conflict resolution", "strategic thinking", "emotional intelligence",
    "decision making", "negotiation", "attention to detail", "customer service", "presentation",
    "multitasking", "self-motivation", "organization"
]

tools_keywords = [
    "python", "java", "c++", "javascript", "typescript", "react", "angular", "vue",
    "node", "express", "django", "flask", "spring", "git", "github", "gitlab",
    "docker", "kubernetes", "aws", "azure", "gcp", "postgresql", "mysql", "mongodb",
    "redis", "linux", "jira", "confluence", "notion", "slack", "excel", "powerpoint",
    "tableau", "power bi", "spark", "hadoop", "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "matplotlib", "figma", "photoshop", "illustrator"
]

experience_keywords = [
    "worked at", "experience", "background", "internship", "previous role", "former company",
    "professional history", "career", "projects", "employment", "responsible for",
    "job title", "as a", "consulted for", "managed", "handled", "developed", "led team",
    "collaborated", "participated", "contributed", "in charge of", "was part of"
]

############
## functions
############

def extract_elements(transcript: str) -> dict:
    doc = nlp(transcript.lower())
    skills_found = set()
    tools_found = set()
    experience_phrases = []

    for sent in doc.sents:
        sent_text = sent.text.strip()
        lemmatized = " ".join([token.lemma_ for token in sent])

        for kw in skills_keywords:
            if kw in lemmatized:
                skills_found.add(kw)

        for tool in tools_keywords:
            if tool in sent_text:
                tools_found.add(tool)

        if any(exp in lemmatized for exp in experience_keywords):
            experience_phrases.append(sent_text)

    return {
        "skills": sorted(skills_found),
        "tools": sorted(tools_found),
        "experience_phrases": experience_phrases
    }
