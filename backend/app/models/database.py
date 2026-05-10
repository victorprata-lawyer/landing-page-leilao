from pathlib import Path
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

root_path = Path(__file__).resolve().parents[3]

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_PATH = root_path / "assets.db"

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
else:
    engine = create_engine(
        f"sqlite:///{DATABASE_PATH}",
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    from app.models.models import Base
    Base.metadata.create_all(bind=engine)