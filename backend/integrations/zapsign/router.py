from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .schemas import WebhookPayload
from .service import process_webhook
from app.models.database import get_db

router = APIRouter()

@router.post("/webhooks/zapsign")
def zapsign_webhook_handler(payload: WebhookPayload, db: Session = Depends(get_db)):
    # Processa webhook do ZapSign
    return process_webhook(db, payload)