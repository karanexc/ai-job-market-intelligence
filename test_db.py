from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:996765@localhost:5432/job_market_db"

engine = create_engine(DATABASE_URL)

try:
    conn = engine.connect()
    print("Database connected successfully!")
    conn.close()
except Exception as e:
    print("Error:", e)