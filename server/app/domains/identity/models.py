from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class User:
    id: UUID
    display_name: str
    password_hash: str
    role: str
    is_active: bool
    created_at: datetime
