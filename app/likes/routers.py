from fastapi import APIRouter, Depends, HTTPException

from app.likes.dao import LikeDAO
from app.user.auth import get_current_user
from app.user.models import User

router = APIRouter(prefix="/likes", tags=["Likes"])

@router.post("/{tweet_id}")
async def like_tweet(tweet_id: int, user: User = Depends(get_current_user)):
    if await LikeDAO.is_liked(tweet_id, user.id):
        raise HTTPException(status_code=400, detail="Already liked")
    await LikeDAO.add_like(tweet_id, user.id)
    return {"detail": "Tweet liked"}

@router.delete("/{tweet_id}")
async def unlike_tweet(tweet_id: int, user: User = Depends(get_current_user)):
    if not await LikeDAO.is_liked(tweet_id, user.id):
        raise HTTPException(status_code=400, detail="Not liked yet")
    await LikeDAO.remove_like(tweet_id, user.id)
    return {"detail": "Tweet unliked"}