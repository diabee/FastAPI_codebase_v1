import os
import time
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Load .env from config directory (relative to this file's location)
env_path = Path(__file__).resolve().parent.parent.parent / "config" / ".env"
load_dotenv(env_path)

engine = create_engine(
    os.getenv("MYSQL_HOST"),
    pool_pre_ping=True,
    pool_size=int(os.getenv("POOL_SIZE", 32)),
    max_overflow=int(os.getenv("MAX_OVERFLOW", 64)),
    echo=(os.getenv("DEBUG", "False") == "True"),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db_session():
    """Create database session and yield it"""
    retries = 3
    delay = 2
    for i in range(retries):
        db = SessionLocal()
        try:
            yield db
            break
        except OperationalError:
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise
        finally:
            try:
                db.close()
            except OperationalError:
                pass


def close_db_session(db_session):
    """Close database session"""
    try:
        db_session.close()
    except Exception:
        db_session.rollback()
        raise


# Uncomment to auto-create tables
# Base.metadata.create_all(engine)
