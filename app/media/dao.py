from sqlalchemy import select
from app.media.models import Media
from app.database import async_session_maker
from app.dao.base import BaseDao

class MediaDAO(BaseDao):
    model = Media

    @classmethod
    async def create(cls, tweet_id: int, media_url: str):
        async with async_session_maker() as session:
            media = Media(tweet_id=tweet_id, media_url=media_url)
            session.add(media)
            await session.commit()
            await session.refresh(media)
            return media

    @classmethod
    async def get_by_tweet(cls, tweet_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.tweet_id == tweet_id)
            result = await session.execute(query)
            return result.scalars().all()