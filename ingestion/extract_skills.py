import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

from nlp.skill_extractor import extract_skills


# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


def extract_and_store_skills():

    print("Loading jobs from database...")

    query = """
    SELECT job_id, job_title, job_description
    FROM jobs
    """

    jobs_df = pd.read_sql(query, engine)

    print(f"Total jobs loaded: {len(jobs_df)}")

    processed_jobs = 0
    total_skills = 0

    with engine.begin() as conn:

        for _, row in jobs_df.iterrows():

            job_id = row["job_id"]
            title = row["job_title"] or ""
            description = row["job_description"] or ""

            # Combine text fields
            combined_text = f"{title} {description}"

            skills = extract_skills(combined_text)

            if not skills:
                continue

            processed_jobs += 1

            for skill in skills:

                # Insert skill if it doesn't exist
                conn.execute(
                    text("""
                    INSERT INTO skills (skill_name)
                    VALUES (:skill)
                    ON CONFLICT (skill_name) DO NOTHING
                    """),
                    {"skill": skill}
                )

                # Retrieve skill_id
                result = conn.execute(
                    text("""
                    SELECT skill_id
                    FROM skills
                    WHERE skill_name = :skill
                    """),
                    {"skill": skill}
                )

                skill_id = result.fetchone()[0]

                # Insert job-skill mapping (avoid duplicates)
                conn.execute(
                    text("""
                    INSERT INTO job_skills (job_id, skill_id)
                    VALUES (:job_id, :skill_id)
                    ON CONFLICT DO NOTHING
                    """),
                    {"job_id": job_id, "skill_id": skill_id}
                )

                total_skills += 1

    print("\nSkill extraction completed!")
    print(f"Jobs with detected skills: {processed_jobs}")
    print(f"Total skill mappings created: {total_skills}")


if __name__ == "__main__":
    extract_and_store_skills()