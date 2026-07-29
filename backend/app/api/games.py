from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.game import Game
from app.schemas.game import GamePublic
from app.services.rawg_client import rawg_client

router = APIRouter(prefix="/games", tags=["games"])


def _rawg_payload_to_game_fields(payload: dict) -> dict:
    """Converte o payload cru do RAWG nos campos do nosso modelo Game."""
    genres = payload.get("genres") or []
    # em resultados de busca vem "platforms": [{"platform": {"name": ...}}]
    platforms = [
        p.get("platform", {}).get("name")
        for p in (payload.get("platforms") or [])
        if p.get("platform", {}).get("name")
    ]

    released = payload.get("released")  # RAWG retorna string "YYYY-MM-DD" ou None
    release_dt = None
    if released:
        try:
            release_dt = datetime.strptime(released, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            release_dt = None

    return {
        "rawg_id": payload["id"],
        "name": payload.get("name", ""),
        # a busca não traz descrição longa; o detalhe (get_game_by_id) traz em "description_raw"
        "summary": payload.get("description_raw"),
        "cover_url": payload.get("background_image"),
        "first_release_date": release_dt,
        "genres": ",".join(g["name"] for g in genres if "name" in g),
        "platforms": ",".join(platforms),
        "rawg_rating": payload.get("rating"),
    }


def _get_or_cache_game(session: Session, rawg_payload: dict) -> Game:
    """Busca o jogo no cache local; se não existir, cria a partir do payload do RAWG."""
    game = session.exec(
        select(Game).where(Game.rawg_id == rawg_payload["id"])
    ).first()
    if game:
        return game

    game = Game(**_rawg_payload_to_game_fields(rawg_payload))
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


@router.get("/search", response_model=list[GamePublic])
async def search_games(
    q: str = Query(..., min_length=2),
    session: Session = Depends(get_session),
):
    """
    Busca jogos por nome. Consulta o RAWG e cacheia os resultados localmente.
    """
    try:
        results = await rawg_client.search_games(q)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    games = [_get_or_cache_game(session, r) for r in results]
    return games


@router.get("/{rawg_id}", response_model=GamePublic)
async def get_game(rawg_id: int, session: Session = Depends(get_session)):
    """
    Retorna os detalhes de um jogo. Usa o cache local se já existir,
    senão busca no RAWG e cacheia.
    """
    game = session.exec(select(Game).where(Game.rawg_id == rawg_id)).first()
    if game:
        return game

    try:
        payload = await rawg_client.get_game_by_id(rawg_id)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    if not payload:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    return _get_or_cache_game(session, payload)
