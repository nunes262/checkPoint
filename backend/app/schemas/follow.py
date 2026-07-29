from pydantic import BaseModel


class FollowStatus(BaseModel):
    following: bool
    followers_count: int
    following_count: int
