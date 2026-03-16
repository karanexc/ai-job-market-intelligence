import pandas as pd
from sqlalchemy import create_engine, text
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


country_map = {
    "san francisco": ("US", "North America"),
    "sf": ("US", "North America"),
    "seattle": ("US", "North America"),
    "nyc": ("US", "North America"),
    "new york": ("US", "North America"),
    "us": ("US", "North America"),

    "canada": ("Canada", "North America"),
    "toronto": ("Canada", "North America"),

    "mexico": ("Mexico", "North America"),
    "mexico city": ("Mexico", "North America"),

    "singapore": ("Singapore", "Asia"),

    "india": ("India", "Asia"),
    "bangalore": ("India", "Asia"),
    "bengaluru": ("India", "Asia"),

    "uk": ("UK", "Europe"),
    "united kingdom": ("UK", "Europe"),
    "london": ("UK", "Europe"),

    "germany": ("Germany", "Europe"),
    "berlin": ("Germany", "Europe"),

    "ireland": ("Ireland", "Europe"),
    "dublin": ("Ireland", "Europe"),

    "romania": ("Romania", "Europe"),
    "bucharest": ("Romania", "Europe"),

    "spain": ("Spain", "Europe"),
    "barcelona": ("Spain", "Europe")
}


def normalize_location(location):

    if location is None:
        return None, None

    location = location.lower()

    for key in country_map:

        if key in location:
            return country_map[key]

    if "remote" in location or "world" in location:
        return "Global", "Global"

    if "worldwide" in location:
        return "Global", "Global"

    return None, None


def run():

    print("Loading jobs...")

    df = pd.read_sql("SELECT job_id, company_location FROM jobs", engine)

    print("Total jobs:", len(df))

    updates = []

    for _, row in df.iterrows():

        country, region = normalize_location(row["company_location"])

        if country:

            updates.append({
                "job_id": row["job_id"],
                "country": country,
                "region": region
            })

    updates_df = pd.DataFrame(updates)

    print("Rows to update:", len(updates_df))

    with engine.begin() as conn:

        for _, row in updates_df.iterrows():

            conn.execute(
                text("""
                    UPDATE jobs
                    SET country = :country,
                        region = :region
                    WHERE job_id = :job_id
                """),
                {
                    "country": row["country"],
                    "region": row["region"],
                    "job_id": int(row["job_id"])
                }
            )

    print("Location normalization complete!")


if __name__ == "__main__":
    run()