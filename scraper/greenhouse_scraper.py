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


companies = [
    "stripe",
    "airbnb",
    "openai",
    "robinhood",
    "coinbase",
    "databricks",
    "notion",
    "figma",
    "discord",
    "dropbox"
]


def scrape_greenhouse():

    jobs = []

    for company in companies:

        url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

        print("Scraping:", url)

        response = requests.get(url)

        if response.status_code != 200:
            print("Skipping (API not available)")
            continue

        data = response.json()

        if "jobs" not in data:
            print("No jobs found for", company)
            continue

        for job in data["jobs"]:

            jobs.append({
                "job_title": job.get("title"),
                "company_name": company,
                "company_location": job.get("location", {}).get("name"),
                "job_url": job.get("absolute_url"),
                "source": "greenhouse"
            })

    df = pd.DataFrame(jobs)

    print("\nTotal jobs scraped:", len(df))
    print(df.head())

    return df


if __name__ == "__main__":

    df = scrape_greenhouse()

    df.to_sql(
        "jobs",
        engine,
        if_exists="append",
        index=False
    )

    print("Jobs saved to PostgreSQL")