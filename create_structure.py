import os

folders = [
    "data/raw",
    "data/processed",
    "database",
    "ingestion",
    "nlp",
    "ml",
    "analytics",
    "api",
    "dashboard",
    "utils"
]

files = [
    "requirements.txt",
    "README.md",
    "database/schema.sql",
    "database/db_connection.py",
    "ingestion/load_jobs.py",
    "ingestion/clean_jobs.py",
    "ingestion/extract_skills.py",
    "nlp/skill_extractor.py",
    "nlp/skill_dictionary.py",
    "ml/salary_model.py",
    "ml/trend_analysis.py",
    "analytics/skill_demand.py",
    "analytics/career_recommender.py",
    "api/main.py",
    "api/routes.py",
    "dashboard/app.py",
    "utils/config.py",
    "utils/helpers.py"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    os.makedirs(os.path.dirname(file), exist_ok=True)
    open(file, "a").close()

print("Project structure created in current directory.")