from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.exc import SQLAlchemyError

from app.media.dao import MediaDAO
from app.tweet.dao import TweetDAO
from app.tweet.schemas import TweetCreate, TweetResponse, TweetCreatedResponse
from app.user.auth import get_current_user
from app.user.models import User

router = APIRouter(
    prefix="/api/tweets",
    tags=["Tweets"]
)

@router.post("/", response_model=TweetCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_tweet(
    tweet_data: TweetCreate,
    current_user: User = Depends(get_current_user)
):
    try:
        tweet = await TweetDAO.create(
            content=tweet_data.tweet_data,
            author_id=current_user.id,
            media_ids=tweet_data.tweet_media_ids
        )
        return {
            "result": True,
            "tweet_id": tweet.id
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create tweet"
        )


@router.delete("/{tweet_id}", status_code=status.HTTP_200_OK)
async def delete_tweet(
    tweet_id: int,
    current_user: User = Depends(get_current_user)
):
    deleted = await TweetDAO.delete(tweet_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tweet not found or unauthorized")
    return {"result": True}


@router.post("/{tweet_id}/likes", status_code=status.HTTP_200_OK)
async def like_tweet(
    tweet_id: int,
    current_user: User = Depends(get_current_user)
):
    success = await TweetDAO.add_like(tweet_id, current_user.id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not like tweet")
    return {"result": True}


@router.delete("/{tweet_id}/likes", status_code=status.HTTP_200_OK)
async def unlike_tweet(
    tweet_id: int,
    current_user: User = Depends(get_current_user)
):
    success = await TweetDAO.remove_like(tweet_id, current_user.id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not unlike tweet")
    return {"result": True}


