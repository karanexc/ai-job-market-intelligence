import pandas as pd
import matplotlib.pyplot as plt
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


def get_skill_demand():

    query = """
    SELECT s.skill_name, COUNT(js.job_id) AS demand
    FROM skills s
    JOIN job_skills js ON s.skill_id = js.skill_id
    GROUP BY s.skill_name
    ORDER BY demand DESC
    """

    df = pd.read_sql(query, engine)

    print(df.head(10))

    # Plot top 10 skills
    top_skills = df.head(10)

    plt.figure(figsize=(10,6))
    plt.bar(top_skills["skill_name"], top_skills["demand"])
    plt.xticks(rotation=45)
    plt.title("Top Skills in Job Market")
    plt.xlabel("Skill")
    plt.ylabel("Demand")

    plt.show()


if __name__ == "__main__":
    get_skill_demand()