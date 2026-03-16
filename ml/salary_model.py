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


def salary_by_skill():

    query = """
    SELECT s.skill_name,
           AVG(j.salary_in_usd) AS avg_salary
    FROM skills s
    JOIN job_skills js ON s.skill_id = js.skill_id
    JOIN jobs j ON js.job_id = j.job_id
    GROUP BY s.skill_name
    ORDER BY avg_salary DESC
    """

    df = pd.read_sql(query, engine)

    print(df.head(10))

    # Visualization
    top = df.head(10)

    plt.figure(figsize=(10,6))
    plt.bar(top["skill_name"], top["avg_salary"])
    plt.xticks(rotation=45)
    plt.title("Average Salary by Skill")
    plt.xlabel("Skill")
    plt.ylabel("Average Salary (USD)")

    plt.show()


if __name__ == "__main__":
    salary_by_skill()