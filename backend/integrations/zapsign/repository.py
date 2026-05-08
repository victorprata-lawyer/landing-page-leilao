from sqlalchemy.orm import Session
import datetime
from typing import Optional
from .schemas import WebhookPayload

# Ajuste o caminho do import de Ativo conforme a estrutura do seu projeto
from app.models import Ativo

def _parse_iso_datetime(dt_str: str) -> datetime.datetime:
    """Parse string ISO para datetime."""
    if dt_str.endswith('Z'):
        dt_str = dt_str[:-1] + '+00:00'
    return datetime.datetime.fromisoformat(dt_str)

def buscar_ativo_por_zapsign_document_id(session: Session, zapsign_document_id: str) -> Optional[Ativo]:
    """Busca Ativo pelo zapsign_document_id."""
    return session.query(Ativo).filter(Ativo.zapsign_document_id == zapsign_document_id).first()

def processar_formalizacao_webhook(session: Session, payload: WebhookPayload) -> Optional[Ativo]:
    """Processa webhook de formalização do ZapSign."""
    ativo = buscar_ativo_por_zapsign_document_id(session, payload.document_id)
    if not ativo:
        return None

    try:
        ativo.status = 'Fluxo Protegido Formalizado'
        ativo.data_formalizacao = _parse_iso_datetime(payload.signed_at)
        email_signatario = payload.signer_email or (payload.signers[0].email if payload.signers else None)
        if email_signatario:
            ativo.email_signatario = email_signatario
        session.commit()
        session.refresh(ativo)
        return ativo
    except Exception:
        session.rollback()
        raise