import streamlit as st
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

st.title("AI Job Market Intelligence Dashboard")

st.header("Top Skills in Job Market")

skill_query = """
SELECT s.skill_name, COUNT(js.job_id) AS demand
FROM skills s
JOIN job_skills js ON s.skill_id = js.skill_id
GROUP BY s.skill_name
ORDER BY demand DESC
"""

skills_df = pd.read_sql(skill_query, engine)

st.dataframe(skills_df)

st.bar_chart(skills_df.set_index("skill_name"))

st.header("Average Salary by Skill")

salary_query = """
SELECT s.skill_name,
       AVG(j.salary_in_usd) AS avg_salary
FROM skills s
JOIN job_skills js ON s.skill_id = js.skill_id
JOIN jobs j ON js.job_id = j.job_id
GROUP BY s.skill_name
ORDER BY avg_salary DESC
"""

salary_df = pd.read_sql(salary_query, engine)

st.dataframe(salary_df)

st.bar_chart(salary_df.set_index("skill_name"))