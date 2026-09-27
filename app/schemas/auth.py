from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Validade do token em segundos.")


class TokenPayload(BaseModel):
    sub: str
    scopes: list[str] = []
    jti: str | None = None


class UserPublic(BaseModel):
    username: str
    full_name: str | None = None
    role: str


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1)
    grant_type: str | None = None
    scope: str = ""
    client_id: str | None = None
    client_secret: str | None = None
