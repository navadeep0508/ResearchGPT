from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

DATABASE_URL = (
    "postgresql://researchgpt_db_user:b9hodqEeEhm25DnRTRyHSONJ9JiW4WjH@dpg-d87b3vcm0tmc739nn070-a/researchgpt_db"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()