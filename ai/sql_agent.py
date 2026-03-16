import os
from openai import OpenAI
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


def generate_sql(question):

    prompt = f"""
You are an AI that converts user questions into PostgreSQL queries.

Database schema:

jobs(
job_id,
job_title,
company_name,
company_location,
region,
experience_level,
employment_type,
salary_in_usd,
remote_ratio,
company_size,
job_description,
job_url,
date_posted,
source
)

skills(
skill_id,
skill_name
)

job_skills(
id,
job_id,
skill_id
)

Relationships:
jobs.job_id = job_skills.job_id
skills.skill_id = job_skills.skill_id

Important rules:

1. Use fuzzy matching with ILIKE.

Example:
skill_name ILIKE '%machine learning%'

2. If the user mentions a skill that may not exist exactly
(e.g. "aiml", "ml", "genai"), search related skills.

Examples:
aiml → ai OR machine learning
ml → machine learning
genai → generative ai OR ai

3. If no skill match is obvious, search job_title instead.

Example:
job_title ILIKE '%machine learning%'

4. When filtering by region use:

jobs.region = 'Europe'

5. Always join the tables when searching skills.

Example:

FROM jobs j
JOIN job_skills js ON j.job_id = js.job_id
JOIN skills s ON js.skill_id = s.skill_id

6. Limit results to 50 rows unless aggregation is requested.

7. Return ONLY SQL.
Do NOT include ``` or explanations.

User question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response.choices[0].message.content.strip()

    # Clean markdown if model adds it
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql


def run_query(sql):

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()

    return rows


def ask(question):

    sql = generate_sql(question)

    print("\nGenerated SQL:\n")
    print(sql)

    result = run_query(sql)

    return result