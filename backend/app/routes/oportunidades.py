from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
from app.models.database import get_db

router = APIRouter(prefix="/api/oportunidades", tags=["oportunidades"])

@router.get("/")
def listar_oportunidades(db: Session = Depends(get_db)):
    try:
        # Busca os dados brutos do banco assets.db
        query = text("SELECT * FROM assets ORDER BY avaliacao DESC")
        result = db.execute(query)
        
        oportunidades_formatadas = []
        
        for row in result:
            data = dict(row._mapping)
            
            # MAPEAMENTO ESSENCIAL: De Banco (PT) para Frontend (EN)
            item = {
                "public_code": data.get("public_code") or data.get("process_number") or "PR-000",
                "city": data.get("cidade") or data.get("city") or "N/A",
                "state": data.get("estado") or data.get("state") or "N/A",
                "typology": data.get("tipo") or data.get("typology") or "Imóvel",
                "estimated_vgv": float(data.get("avaliacao") or 0),
                "min_bid": float(data.get("arremate") or 0),
                "status": data.get("status", "Disponível")
            }
            oportunidades_formatadas.append(item)
            
        return oportunidades_formatadas
        
    except Exception as e:
        logging.error(f"Erro ao listar oportunidades: {e}")
        return {"error": str(e)}