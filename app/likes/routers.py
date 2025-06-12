from fastapi import APIRouter, Depends, HTTPException, Header

from app.likes.dao import LikeDAO
from app.user.auth import get_current_user
from app.user.dao import UserDAO
from app.user.models import User

router = APIRouter(prefix="/api/tweets", tags=["Likes"])

@router.post("/{tweet_id}/likes")
async def like_tweet(tweet_id: int, api_key: str = Header(...)):
    user = await UserDAO.find_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if await LikeDAO.is_liked(tweet_id, user.id):
        raise HTTPException(status_code=400, detail="Already liked")
    await LikeDAO.like_tweet(tweet_id, user.id)
    return {"result": "True"}

@router.delete("/{tweet_id}/likes")
async def unlike_tweet(tweet_id: int, api_key: str = Header(...)):
    user = await UserDAO.find_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not await LikeDAO.is_liked(tweet_id, user.id):
        raise HTTPException(status_code=400, detail="Not liked yet")
    await LikeDAO.unlike_tweet(tweet_id, user.id)
    return {"result": "True"}