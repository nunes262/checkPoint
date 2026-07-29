from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class ReviewLike(SQLModel, table=True):
    __tablename__ = "review_likes"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, nullable=False)
    review_id: int = Field(foreign_key="reviews.id", index=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
