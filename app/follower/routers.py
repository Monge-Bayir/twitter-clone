from fastapi import APIRouter, HTTPException, Header

from app.follower.dao import FollowerDAO
from app.user.dao import UserDAO

router = APIRouter(prefix="/api/users", tags=["Followers"])

@router.post("/{user_id}/follow")
async def follow_user(user_id: int, api_key: str = Header(...)):
    user = await UserDAO.find_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    if await FollowerDAO.is_following(user.id, user_id):
        raise HTTPException(status_code=400, detail="Already following")
    await FollowerDAO.follow(user.id, user_id)
    return {"result": "True"}

@router.delete("/{user_id}/follow")
async def unfollow_user(user_id: int, api_key: str = Header(...)):
    user = await UserDAO.find_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not await FollowerDAO.is_following(user.id, user_id):
        raise HTTPException(status_code=400, detail="You are not following this user")
    await FollowerDAO.unfollow(user.id, user_id)
    return {"result": "True"}