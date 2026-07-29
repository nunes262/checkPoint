from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.api.reviews import _to_public
from app.db.session import get_session
from app.models.follow import Follow
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewPublic

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("", response_model=list[ReviewPublic])
def get_feed(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    limit: int = 30,
):
    """
    Retorna as reviews mais recentes das pessoas que o usuário atual segue.
    """
    following_ids = session.exec(
        select(Follow.following_id).where(Follow.follower_id == current_user.id)
    ).all()

    if not following_ids:
        return []

    reviews = session.exec(
        select(Review)
        .where(Review.user_id.in_(following_ids))
        .order_by(Review.created_at.desc())
        .limit(limit)
    ).all()

    return [_to_public(session, r) for r in reviews]
