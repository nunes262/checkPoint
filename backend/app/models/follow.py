from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Follow(SQLModel, table=True):
    """
    Relação de "seguir" entre usuários.
    follower_id segue follows_id.
    """
    __tablename__ = "follows"

    id: Optional[int] = Field(default=None, primary_key=True)
    follower_id: int = Field(foreign_key="users.id", index=True, nullable=False)
    following_id: int = Field(foreign_key="users.id", index=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
