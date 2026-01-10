from __future__ import annotations

import uuid
from datetime import datetime

from sqlmodel import SQLModel


class RegisterPayload(SQLModel):
    display_name: str
    password: str
    role: str = "reader"


class BootstrapPayload(SQLModel):
    display_name: str
    password: str


class LoginPayload(SQLModel):
    display_name: str
    password: str


class AuthUser(SQLModel):
    id: uuid.UUID
    display_name: str
    role: str
    is_active: bool
    created_at: datetime


class AuthToken(SQLModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUser
