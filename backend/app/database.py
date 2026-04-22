from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Importação direta do arquivo models que está na mesma pasta
from app.models import Base 

# O banco será criado na raiz do projeto
engine = create_engine('sqlite:///assets.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)