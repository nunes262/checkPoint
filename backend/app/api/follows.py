from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.follow import Follow
from app.models.user import User
from app.schemas.follow import FollowStatus
from app.schemas.user import UserPublic

router = APIRouter(prefix="/users", tags=["follows"])


@router.post("/{user_id}/follow", status_code=204)
def follow_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Você não pode seguir a si mesmo")

    target = session.get(User, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    existing = session.exec(
        select(Follow).where(
            Follow.follower_id == current_user.id, Follow.following_id == user_id
        )
    ).first()
    if existing:
        return  # já segue, idempotente

    session.add(Follow(follower_id=current_user.id, following_id=user_id))
    session.commit()


@router.delete("/{user_id}/follow", status_code=204)
def unfollow_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    existing = session.exec(
        select(Follow).where(
            Follow.follower_id == current_user.id, Follow.following_id == user_id
        )
    ).first()
    if existing:
        session.delete(existing)
        session.commit()


@router.get("/{user_id}/follow-status", response_model=FollowStatus)
def follow_status(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    following = session.exec(
        select(Follow).where(
            Follow.follower_id == current_user.id, Follow.following_id == user_id
        )
    ).first()
    followers_count = session.exec(
        select(func.count()).select_from(Follow).where(Follow.following_id == user_id)
    ).one()
    following_count = session.exec(
        select(func.count()).select_from(Follow).where(Follow.follower_id == user_id)
    ).one()
    return FollowStatus(
        following=bool(following),
        followers_count=followers_count,
        following_count=following_count,
    )


@router.get("/{user_id}/followers", response_model=list[UserPublic])
def list_followers(user_id: int, session: Session = Depends(get_session)):
    follows = session.exec(select(Follow).where(Follow.following_id == user_id)).all()
    return [session.get(User, f.follower_id) for f in follows]


@router.get("/{user_id}/following", response_model=list[UserPublic])
def list_following(user_id: int, session: Session = Depends(get_session)):
    follows = session.exec(select(Follow).where(Follow.follower_id == user_id)).all()
    return [session.get(User, f.following_id) for f in follows]
