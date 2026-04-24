import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import wellness, oportunidades
from app.models.database import create_tables

# Configuração de diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Carrega variáveis de ambiente
load_dotenv()

# Instância FastAPI (apenas uma vez)
app = FastAPI()

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pratarealestate.com.br",
        "https://www.pratarealestate.com.br",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria tabelas se não for Vercel
if "VERCEL" not in os.environ:
    try:
        create_tables()
    except Exception as e:
        print(f"Aviso: Erro ao criar tabelas: {e}")

# Inclui roteadores
app.include_router(wellness.router)
app.include_router(oportunidades.router)

# Rota raiz
@app.get("/")
def read_root():
    return {
        "message": "API Wellness e Oportunidades",
        "status": "ok",
        "version": "1.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# Rota health
@app.get("/health")
def health():
    return {"status": "healthy"}

# Bloco para execução local
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)