from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GamePublic(BaseModel):
    id: int
    rawg_id: int
    name: str
    summary: Optional[str] = None
    cover_url: Optional[str] = None
    first_release_date: Optional[datetime] = None
    genres: Optional[str] = None
    platforms: Optional[str] = None
    rawg_rating: Optional[float] = None

    class Config:
        from_attributes = True
