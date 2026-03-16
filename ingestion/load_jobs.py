import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def load_jobs():

    file_path = "data/raw/ds_salaries.csv"

    df = pd.read_csv(file_path)

    df = df[[
        "job_title",
        "company_location",
        "experience_level",
        "employment_type",
        "salary_in_usd",
        "remote_ratio",
        "company_size"
    ]]

    df.to_sql(
        "jobs",
        engine,
        if_exists="append",
        index=False
    )

    print("Jobs loaded into database successfully!")


if __name__ == "__main__":
    load_jobs()