from fastapi import APIRouter, Depends, HTTPException

from app.follower.dao import FollowerDAO
from app.user.auth import get_current_user
from app.user.models import User

router = APIRouter(prefix="/follow", tags=["Followers"])

@router.post("/{user_id}")
async def follow_user(user_id: int, user: User = Depends(get_current_user)):
    if user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    if await FollowerDAO.is_following(user.id, user_id):
        raise HTTPException(status_code=400, detail="Already following")
    await FollowerDAO.follow(user.id, user_id)
    return {"detail": f"You are now following user {user_id}"}

@router.delete("/{user_id}")
async def unfollow_user(user_id: int, user: User = Depends(get_current_user)):
    if not await FollowerDAO.is_following(user.id, user_id):
        raise HTTPException(status_code=400, detail="You are not following this user")
    await FollowerDAO.unfollow(user.id, user_id)
    return {"detail": f"You have unfollowed user {user_id}"}