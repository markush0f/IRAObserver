from __future__ import annotations

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError

from app.core.settings import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET_KEY

class TokenPayload(BaseModel):
    sub: str
    role: str
    exp: datetime
    iat: datetime


def _get_secret_key() -> str:
    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is not set")
    return JWT_SECRET_KEY


def _get_algorithm() -> str:
    return JWT_ALGORITHM


def _get_exp_minutes() -> int:
    return JWT_EXPIRE_MINUTES


def create_access_token(subject: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=_get_exp_minutes())
    payload = {"sub": subject, "role": role, "iat": now, "exp": expire}
    return jwt.encode(payload, _get_secret_key(), algorithm=_get_algorithm())


def decode_access_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            _get_secret_key(),
            algorithms=[_get_algorithm()],
        )
        return TokenPayload.model_validate(payload)
    except (JWTError, ValidationError) as exc:
        raise ValueError("invalid token") from exc
