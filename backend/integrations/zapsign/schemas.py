from pydantic import BaseModel
from typing import List, Optional


class Signer(BaseModel):
    email: str


class WebhookPayload(BaseModel):
    event: str
    document_id: str
    signed_at: str  # ISO format expected
    signers: List[Signer]
    signer_email: Optional[str] = None  # Opcional para compatibilidade