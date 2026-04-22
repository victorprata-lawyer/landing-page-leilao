import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base

# CAMINHO ABSOLUTO FORÇADO (Caminho que o seu terminal confirmou ter 880 ativos)
DATABASE_PATH = r"C:\Users\victo\OneDrive\Documentos\advocacia-hub\assets.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Criação do engine com verificação de existência
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    # Isso garante que as tabelas existam no arquivo correto
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()