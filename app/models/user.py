from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(String(64), unique=True, index=True, nullable=False))
    hashed_password: str = Field(sa_column=Column(String(128), nullable=False))
    full_name: str | None = Field(default=None, sa_column=Column(String(120), nullable=True))
    role: str = Field(default="analyst", sa_column=Column(String(32), nullable=False))
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
