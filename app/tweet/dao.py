from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDao
from app.database import async_session_maker
from app.likes.models import Like
from app.tweet.models import Tweet
from sqlalchemy import select
from app.media.models import Media


class TweetDAO(BaseDao):
    model = Tweet

    @classmethod
    async def create(cls, content: str, author_id: int, media_ids: list[int] = None):
        async with async_session_maker() as session:
            tweet = Tweet(
                content=content,
                author_id=author_id,
                created_at=datetime.now()
            )
            session.add(tweet)
            await session.flush()  # нужно получить tweet.id до коммита

            if media_ids:
                result = await session.execute(
                    select(Media).where(Media.id.in_(media_ids))
                )
                medias = result.scalars().all()

                if len(medias) != len(media_ids):
                    raise HTTPException(
                        status_code=400,
                        detail="One or more media IDs are invalid"
                    )

                for media in medias:
                    media.tweet_id = tweet.id

            await session.commit()
            await session.refresh(tweet)
            return tweet

    @classmethod
    async def delete(cls, tweet_id: int, author_id: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(cls.model).where(cls.model.id == tweet_id, cls.model.author_id == author_id)
            )
            tweet = result.scalar_one_or_none()
            if tweet:
                await session.delete(tweet)
                await session.commit()
                return True
            return False

    @classmethod
    async def get_tweet(cls):
        async with async_session_maker() as session:
            result = await session.execute(
                select(Tweet)
                .options(
                    selectinload(Tweet.author),
                    selectinload(Tweet.likes).selectinload(Like.user),
                    selectinload(Tweet.media),
                )
            )
            tweets = result.scalars().all()

        serialized = []
        for tweet in tweets:
            serialized.append({
                "id": tweet.id,
                "content": tweet.content,
                "attachments": [media.file_path for media in tweet.media],
                "author": {
                    "id": tweet.author.id,
                    "name": tweet.author.name
                },
                "likes": [
                    {
                        "user_id": like.user.id,
                        "name": like.user.name
                    } for like in tweet.likes
                ]
            })

        return serialized