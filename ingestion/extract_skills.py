import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

from nlp.skill_extractor import extract_skills

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


def extract_and_store_skills():

    query = "SELECT job_id, job_title FROM jobs"

    jobs_df = pd.read_sql(query, engine)

    with engine.begin() as conn:

        for _, row in jobs_df.iterrows():

            job_id = row["job_id"]
            title = row["job_title"]

            skills = extract_skills(title)

            for skill in skills:

                # Insert skill if not exists
                conn.execute(
                    text("""
                    INSERT INTO skills (skill_name)
                    VALUES (:skill)
                    ON CONFLICT (skill_name) DO NOTHING
                    """),
                    {"skill": skill}
                )

                # Get skill id
                result = conn.execute(
                    text("""
                    SELECT skill_id FROM skills
                    WHERE skill_name = :skill
                    """),
                    {"skill": skill}
                )

                skill_id = result.fetchone()[0]

                # Insert job-skill mapping
                conn.execute(
                    text("""
                    INSERT INTO job_skills (job_id, skill_id)
                    VALUES (:job_id, :skill_id)
                    """),
                    {"job_id": job_id, "skill_id": skill_id}
                )

    print("Skills extracted and stored successfully!")


if __name__ == "__main__":
    extract_and_store_skills()