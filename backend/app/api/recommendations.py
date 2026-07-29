from collections import Counter

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.game import Game
from app.models.review import Review
from app.models.user import User
from app.schemas.game import GamePublic
from app.services.rawg_client import rawg_client

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("", response_model=list[GamePublic])
async def get_recommendations(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    limit: int = 20,
):
    """
    Recomendação simples: olha os gêneros dos jogos que o usuário avaliou
    e busca outros jogos populares desses mesmos gêneros no RAWG.

    Isso é um ponto de partida — dá pra evoluir depois para algo mais
    sofisticado (ex: levar em conta notas, jogos de quem você segue, etc).
    """
    reviews = session.exec(
        select(Review).where(Review.user_id == current_user.id)
    ).all()

    if not reviews:
        return []

    reviewed_game_ids = [r.game_id for r in reviews]
    games = [session.get(Game, gid) for gid in reviewed_game_ids]

    genre_counter: Counter[str] = Counter()
    for g in games:
        if g and g.genres:
            genre_counter.update(g.genres.split(","))

    if not genre_counter:
        return []

    top_genre_name = genre_counter.most_common(1)[0][0]

    # Nota: o RAWG filtra por "slug" de gênero (ex: "action", "role-playing-games-rpg"),
    # não pelo nome exibido. Numa implementação completa vale guardar o slug
    # junto ao nome no cache do Game (hoje o modelo só guarda o nome como string).
    # Fica como próximo passo. Por ora, usamos busca por nome como placeholder.
    results = await rawg_client.search_games(top_genre_name, limit=limit)

    from app.api.games import _get_or_cache_game
    return [_get_or_cache_game(session, r) for r in results]
