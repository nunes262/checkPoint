from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.game import Game
from app.models.like import ReviewLike
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewPublic, ReviewUpdate
from app.services.rawg_client import rawg_client
from app.api.games import _get_or_cache_game

router = APIRouter(prefix="/reviews", tags=["reviews"])


def _to_public(session: Session, review: Review) -> ReviewPublic:
    likes_count = session.exec(
        select(func.count()).select_from(ReviewLike).where(ReviewLike.review_id == review.id)
    ).one()
    user = session.get(User, review.user_id)
    game = session.get(Game, review.game_id)
    return ReviewPublic(
        id=review.id,
        rating=review.rating,
        text=review.text,
        contains_spoilers=review.contains_spoilers,
        created_at=review.created_at,
        updated_at=review.updated_at,
        user=user,
        game=game,
        likes_count=likes_count,
    )


@router.post("", response_model=ReviewPublic, status_code=201)
async def create_review(
    payload: ReviewCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # garante que o jogo existe no cache local, buscando no RAWG se necessário
    game = session.exec(
        select(Game).where(Game.rawg_id == payload.game_rawg_id)
    ).first()
    if not game:
        rawg_payload = await rawg_client.get_game_by_id(payload.game_rawg_id)
        if not rawg_payload:
            raise HTTPException(status_code=404, detail="Jogo não encontrado no RAWG")
        game = _get_or_cache_game(session, rawg_payload)

    existing_review = session.exec(
        select(Review).where(
            Review.user_id == current_user.id,
            Review.game_id == game.id,
        )
    ).first()
    if existing_review:
        raise HTTPException(
            status_code=409,
            detail="Você já possui uma review para este jogo",
        )

    review = Review(
        user_id=current_user.id,
        game_id=game.id,
        rating=payload.rating,
        text=payload.text,
        contains_spoilers=payload.contains_spoilers,
    )
    session.add(review)
    session.commit()
    session.refresh(review)
    return _to_public(session, review)


@router.patch("/{review_id}", response_model=ReviewPublic)
def update_review(
    review_id: int,
    payload: ReviewUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    review = session.get(Review, review_id)
    if not review or review.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Review não encontrada")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)
    review.updated_at = datetime.now(timezone.utc)

    session.add(review)
    session.commit()
    session.refresh(review)
    return _to_public(session, review)


@router.delete("/{review_id}", status_code=204)
def delete_review(
    review_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    review = session.get(Review, review_id)
    if not review or review.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Review não encontrada")
    session.delete(review)
    session.commit()


@router.get("/game/{rawg_id}", response_model=list[ReviewPublic])
def list_reviews_for_game(rawg_id: int, session: Session = Depends(get_session)):
    game = session.exec(select(Game).where(Game.rawg_id == rawg_id)).first()
    if not game:
        return []
    reviews = session.exec(
        select(Review).where(Review.game_id == game.id).order_by(Review.created_at.desc())
    ).all()
    return [_to_public(session, r) for r in reviews]


@router.post("/{review_id}/like", status_code=204)
def like_review(
    review_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    existing = session.exec(
        select(ReviewLike).where(
            ReviewLike.review_id == review_id, ReviewLike.user_id == current_user.id
        )
    ).first()
    if existing:
        return  # já curtiu, idempotente

    like = ReviewLike(review_id=review_id, user_id=current_user.id)
    session.add(like)
    session.commit()


@router.delete("/{review_id}/like", status_code=204)
def unlike_review(
    review_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    existing = session.exec(
        select(ReviewLike).where(
            ReviewLike.review_id == review_id, ReviewLike.user_id == current_user.id
        )
    ).first()
    if existing:
        session.delete(existing)
        session.commit()
