from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class GameList(SQLModel, table=True):
    """
    Uma lista criada pelo usuário, ex: 'Jogados em 2026', 'Quero jogar', 'Favoritos'.
    """
    __tablename__ = "game_lists"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, nullable=False)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    is_public: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GameListItem(SQLModel, table=True):
    """
    Item dentro de uma GameList, referenciando um jogo.
    """
    __tablename__ = "game_list_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    list_id: int = Field(foreign_key="game_lists.id", index=True, nullable=False)
    game_id: int = Field(foreign_key="games.id", index=True, nullable=False)
    added_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
