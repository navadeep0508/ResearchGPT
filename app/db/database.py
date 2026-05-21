from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

import os
from pathlib import Path
from urllib.parse import urlparse

# Fallback to local SQLite if the URL is empty or points to Render's internal private host (dpg-...)
# which is completely unreachable from outside Render's private network *unless* we are running on Render itself.
db_url = DATABASE_URL
is_render = os.getenv("RENDER") == "true"
is_docker = os.getenv("IN_DOCKER") == "1"
parsed_db_url = urlparse(db_url) if db_url else None
db_host = parsed_db_url.hostname if parsed_db_url else None

if (
    not db_url
    or ("dpg-" in db_url and ".render.com" not in db_url and not is_render)
    or (is_docker and db_host in {"localhost", "127.0.0.1", "::1"})
):
    db_url = "sqlite:///./data/researchgpt.db"

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# SQLite requires different connection args to allow multi-threading in FastAPI
if db_url.startswith("sqlite"):
    db_path = db_url.replace("sqlite:///", "", 1)
    if db_path and db_path != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(db_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
