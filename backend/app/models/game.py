from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Game(SQLModel, table=True):
    """
    Cache local dos dados de jogos vindos do RAWG.
    O campo `rawg_id` é o id original retornado pela API do RAWG.
    Evita bater na API externa toda vez que alguém abre a tela de um jogo.
    """
    __tablename__ = "games"

    id: Optional[int] = Field(default=None, primary_key=True)
    rawg_id: int = Field(index=True, unique=True, nullable=False)
    name: str = Field(index=True, nullable=False)
    summary: Optional[str] = None
    cover_url: Optional[str] = None
    first_release_date: Optional[datetime] = None
    genres: Optional[str] = None  # armazenado como string separada por vírgula, ex: "RPG,Ação"
    platforms: Optional[str] = None
    rawg_rating: Optional[float] = None
    cached_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
