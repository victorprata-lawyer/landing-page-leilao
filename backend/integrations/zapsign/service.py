from sqlalchemy.orm import Session
from typing import Dict

from .schemas import WebhookPayload
from .repository import processar_formalizacao_webhook
from .email_service import send_initial_layer_email


def process_webhook(db: Session, payload: WebhookPayload) -> Dict[str, str]:
    # Eventos que indicam assinatura concluída
    completion_events = {'signature_completed', 'document.completed', 'signed'}

    if payload.event not in completion_events:
        return {"status": "ignored"}

    try:
        # Processa a formalização usando document_id do payload
        ativo = processar_formalizacao_webhook(db, payload)
        if not ativo:
            return {"status": "warn", "message": "Ativo não encontrado"}

        # Extrai e-mail preferencialmente de signer_email ou signers[0]
        signer_email = payload.signer_email or (payload.signers[0].email if payload.signers else None)

        # Envia e-mail inicial
        send_initial_layer_email(ativo.codigo, signer_email)

        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}