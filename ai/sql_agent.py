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
You are a PostgreSQL expert.

Database schema:

jobs(job_id, job_title, company_name, company_location, experience_level,
employment_type, salary_in_usd, remote_ratio, company_size,
job_description, job_url, date_posted, source)

skills(skill_id, skill_name)

job_skills(id, job_id, skill_id)

Write a SQL query to answer the user's question.

Return ONLY SQL. No explanations.

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    sql = response.choices[0].message.content.strip()

    # Remove markdown formatting if the model adds it
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