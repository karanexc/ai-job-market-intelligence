import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


def scrape_remotive():

    records = []

    for page in range(1, 11):

        url = f"https://remotive.com/api/remote-jobs?page={page}"

        print(f"Fetching page {page}")

        response = requests.get(url)

        if response.status_code != 200:
            print("API request failed")
            break

        data = response.json()

        jobs = data.get("jobs", [])

        if not jobs:
            print("No more jobs found")
            break

        for job in jobs:

            records.append({
                "job_title": job.get("title"),
                "company_name": job.get("company_name"),
                "company_location": job.get("candidate_required_location"),
                "job_description": job.get("description"),
                "job_url": job.get("url"),
                "source": "remotive"
            })

    df = pd.DataFrame(records)

    print("\nTotal jobs fetched:", len(df))

    return df


if __name__ == "__main__":

    print("Starting Remotive scraper...\n")

    df = scrape_remotive()

    if len(df) > 0:

        df.to_sql(
            "jobs",
            engine,
            if_exists="append",
            index=False
        )

        print("\nJobs saved to database")

    else:

        print("No jobs scraped")