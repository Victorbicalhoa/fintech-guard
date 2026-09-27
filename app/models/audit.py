from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String
from sqlmodel import SQLModel, Field

class PredictionLog(SQLModel, table=True):
    """Histórico: guarda hash e comprimento, nunca o texto da mensagem.

    username preserva a ownership histórica. Não há renomeação/reutilização
    de usuários nesta API; uma futura alteração exigirá migração para owner_id.
    """
    __tablename__ = "prediction_logs"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(String(64), index=True, nullable=False))
    message_hash: str = Field(sa_column=Column(String(64), nullable=False))
    message_length: int
    predicted_intent: str = Field(sa_column=Column(String(64), nullable=False))
    confidence: float
    risk_level: str = Field(sa_column=Column(String(16), nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), index=True, nullable=False))
