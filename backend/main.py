import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- AJUSTE DE CAMINHO ---
# Define o BASE_DIR como a pasta 'backend' para achar a subpasta 'app'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Agora os imports funcionam sem erro circular
from app.routes import wellness, oportunidades
from app.models.database import create_tables

# Carrega variáveis de ambiente
load_dotenv()

# Instância FastAPI
app = FastAPI()

# Configuração CORS (Mantendo suas URLs originais)
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