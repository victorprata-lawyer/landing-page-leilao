from pathlib import Path
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Localiza a raiz do projeto (advocacia-hub) subindo 3 níveis
root_path = Path(__file__).resolve().parents[3]
DATABASE_PATH = root_path / "assets.db"

# Este print é vital: ele confirmará no seu terminal se o Python achou o arquivo de 344kb
print(f"\n--- CONECTANDO AO BANCO: {DATABASE_PATH} ---")

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
    # Importação interna para evitar erro circular
    from app.models.models import Base
    Base.metadata.create_all(bind=engine)