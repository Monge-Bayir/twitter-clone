from app.dao.base import BaseDao
from app.database import async_session_maker
from app.tweet.models import Tweet
from sqlalchemy import select
from app.media.models import Media


class TweetDAO(BaseDao):
    model = Tweet

    @classmethod
    async def create(cls, content: str, author_id: int, media_ids: list[int] = None):
        async with async_session_maker() as session:
            tweet = Tweet(content=content, author_id=author_id)
            session.add(tweet)
            await session.flush()

            if media_ids:
                result = await session.execute(select(Media).where(Media.id.in_(media_ids)))
                medias = result.scalars().all()
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