from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.game import GamePublic
from app.schemas.user import UserPublic


class ReviewCreate(BaseModel):
    game_rawg_id: int  # id do jogo no RAWG; o backend resolve/cria o cache local
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    text: Optional[str] = None
    contains_spoilers: bool = False


class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    text: Optional[str] = None
    contains_spoilers: Optional[bool] = None


class ReviewPublic(BaseModel):
    id: int
    rating: Optional[float]
    text: Optional[str]
    contains_spoilers: bool
    created_at: datetime
    updated_at: Optional[datetime]
    user: UserPublic
    game: GamePublic
    likes_count: int = 0

    class Config:
        from_attributes = True
