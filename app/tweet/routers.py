from fastapi import APIRouter, HTTPException, status, Header
from sqlalchemy.exc import SQLAlchemyError

from app.tweet.dao import TweetDAO
from app.tweet.schemas import TweetCreate, TweetCreatedResponse
from app.user.dao import UserDAO

router = APIRouter(prefix="/api", tags=["Tweets"])


@router.get("/tweets")
async def get_tweet_feed():
    try:
        tweets = await TweetDAO.get_tweet()
        return {"result": True, "tweets": tweets}

    except Exception as e:
        print("❌ Error while fetching tweets:", repr(e))
        return {
            "result": False,
            "error_type": "InternalServerError",
            "error_message": "Failed to retrieve tweet feed",
        }


@router.post(
    "/tweets", response_model=TweetCreatedResponse, status_code=status.HTTP_201_CREATED
)
async def create_tweet(tweet_data: TweetCreate, api_key: str = Header(...)):
    try:
        user = await UserDAO.find_by_api_key(api_key)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid API key")
        tweet = await TweetDAO.create(
            content=tweet_data.tweet_data,
            author_id=user.id,
            media_ids=tweet_data.tweet_media_ids,
        )
        return {"result": True, "tweet_id": tweet.id}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create tweet",
        )


@router.delete("/tweets/{tweet_id}", status_code=status.HTTP_200_OK)
async def delete_tweet(tweet_id: int, api_key: str = Header(...)):
    user = await UserDAO.find_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    deleted = await TweetDAO.delete(tweet_id, user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tweet not found or unauthorized")
    return {"result": True}
