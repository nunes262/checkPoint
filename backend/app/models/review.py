from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, nullable=False)
    game_id: int = Field(foreign_key="games.id", index=True, nullable=False)
    rating: Optional[float] = Field(default=None, ge=0, le=5)  # nota de 0 a 5, por exemplo
    text: Optional[str] = None
    contains_spoilers: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
