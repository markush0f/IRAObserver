from __future__ import annotations

import uuid
from datetime import datetime

from sqlmodel import SQLModel


class UserCreate(SQLModel):
    display_name: str
    password: str
    role: str = "reader"


class UserPublic(SQLModel):
    id: uuid.UUID
    display_name: str
    role: str
    is_active: bool
    created_at: datetime
