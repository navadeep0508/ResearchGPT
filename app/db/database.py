from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL


db_url = DATABASE_URL

if not db_url:
    raise RuntimeError("DATABASE_URL is not configured.")

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

if not db_url.startswith(("postgresql://", "postgresql+psycopg2://")):
    raise RuntimeError("DATABASE_URL must be a PostgreSQL connection URL.")

engine = create_engine(db_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
