from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.database import get_db

router = APIRouter(prefix="/api/oportunidades", tags=["Oportunidades"])

@router.get("/")
def listar_oportunidades(db: Session = Depends(get_db)):
    try:
        # Forçamos a consulta SQL pura na tabela 'assets' (que o teste confirmou ter 880 linhas)
        query = text("SELECT * FROM assets ORDER BY estimated_vgv DESC")
        result = db.execute(query)
        
        # Convertemos para dicionário para o Frontend entender
        oportunidades = [dict(row._mapping) for row in result]
        
        print(f"--- SUCESSO: {len(oportunidades)} ativos enviados para a Mesa ---")
        return oportunidades
    except Exception as e:
        print(f"--- ERRO NA ROTA: {str(e)} ---")
        return {"error": str(e)}