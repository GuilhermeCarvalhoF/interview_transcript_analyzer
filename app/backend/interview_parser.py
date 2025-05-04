#########
## imports
#########

import re
import spacy
from pathlib import Path

###########
## spacy model
###########

model_path = Path(__file__).parent / "en_core_web_sm/en_core_web_sm-3.8.0"
nlp = spacy.load(model_path)

############
## keywords
############

skills_keywords = [
    "communication", "leadership", "problem-solving", "teamwork", "adaptability",
    "creativity", "collaboration", "time management", "critical thinking", "initiative",
    "analytical thinking", "conflict resolution", "strategic thinking", "emotional intelligence",
    "decision making", "negotiation", "attention to detail", "customer service", "presentation",
    "multitasking", "self-motivation", "organization", "interpersonal skills", "project management",
    "research", "writing", "public speaking", "data analysis", "networking", "mentoring",
    "coaching", "sales", "marketing", "business analysis", "financial analysis", "quality assurance",
    "user experience", "user interface", "graphic design", "web development", "software development",
    "mobile development", "database management", "cloud computing", "cybersecurity", "machine learning",
    "artificial intelligence", "blockchain", "internet of things", "augmented reality",
    "virtual reality", "devops", "agile", "scrum", "kanban", "lean", "six sigma", "design thinking",
    "user research", "usability testing", "wireframing", "prototyping", "A/B testing",
    "search engine optimization", "social media marketing", "content marketing", "email marketing",
    "digital marketing", "brand management", "public relations", "event planning", "fundraising",
    "community engagement", "stakeholder management", "risk management", "change management",
    "business development", "strategic planning", "financial modeling", "budgeting",
    "forecasting", "financial reporting", "accounting", "taxation", "compliance", "auditing",
    "legal research", "contract negotiation", "intellectual property", "litigation",
    "dispute resolution", "employment law", "corporate governance", "mergers and acquisitions"
]

tools_keywords = [
    "python", "java", "c++", "javascript", "typescript", "react", "angular", "vue",
    "node", "express", "django", "flask", "spring", "git", "github", "gitlab",
    "docker", "kubernetes", "aws", "azure", "gcp", "postgresql", "mysql", "mongodb",
    "redis", "linux", "jira", "confluence", "notion", "slack", "excel", "powerpoint",
    "tableau", "power bi", "spark", "hadoop", "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "matplotlib", "figma", "photoshop", "illustrator", "pandas", "numpy",
    "sql", "nosql", "html", "css", "bootstrap", "tailwind", "sass", "less", "graphql",
    "rest", "api", "websocket", "firebase", "heroku", "netlify", "vercel", "aws lambda",
    "azure functions", "gcp cloud functions", "ci/cd", "jenkins", "circleci", "travis",
    "github actions", "bitbucket", "selenium", "cypress", "jest", "mocha", "chai",
    "jasmine", "karma", "webpack", "babel", "eslint", "prettier", "postman", "swagger",
    "apiary", "insomnia", "newman", "docker-compose", "vagrant", "ansible", "puppet",
    "chef", "terraform", "cloudformation", "kustomize", "helm", "prometheus", "grafana",
    "elasticsearch", "kibana", "logstash", "fluentd", "splunk", "datadog", "newrelic",
    "sentry", "rollbar", "raygun", "airflow", "luigi", "celery", "redis queue",
    "rabbitmq", "kafka", "apache beam", "spark streaming", "flink", "druid", "clickhouse",
    "presto", "hive", "pig", "sqoop", "oozie", "zookeeper", "etcd", "consul"
]

experience_keywords = [
    "worked at", "experience", "background", "internship", "previous role", "former company",
    "professional history", "career", "projects", "employment", "responsible for",
    "job title", "as a", "consulted for", "managed", "handled", "developed", "led team",
    "collaborated", "participated", "contributed", "in charge of", "was part of", "created",
    "designed", "implemented", "executed", "coordinated", "oversaw", "directed",
    "supervised", "mentored", "trained", "taught", "guided", "advised", "assisted",
    "supported", "facilitated", "organized", "arranged", "planned", "prepared",
    "conducted", "performed", "executed", "delivered", "achieved", "accomplished",
    "completed", "fulfilled", "succeeded", "attained", "reached", "realized",
    "obtained", "secured", "acquired", "earned", "gained", "won", "received",
    "awarded", "recognized", "acknowledged", "certified", "qualified", "licensed",
    "registered", "accredited", "endorsed", "validated", "verified", "authenticated",
    "approved", "accepted", "ratified", "confirmed", "sanctioned", "authorized"
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
