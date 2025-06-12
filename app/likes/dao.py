from sqlalchemy import select, and_
from app.likes.models import Like
from app.database import async_session_maker
from app.dao.base import BaseDao


class LikeDAO(BaseDao):
    model = Like

    @classmethod
    async def like_tweet(cls, tweet_id: int, user_id: int):
        async with async_session_maker() as session:
            like = Like(tweet_id=tweet_id, user_id=user_id)
            session.add(like)
            await session.commit()
            await session.refresh(like)
            return like

    @classmethod
    async def unlike_tweet(cls, tweet_id: int, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(
                and_(cls.model.tweet_id == tweet_id, cls.model.user_id == user_id)
            )
            result = await session.execute(query)
            like = result.scalar_one_or_none()
            if like:
                await session.delete(like)
                await session.commit()
                return True
            return False

    @classmethod
    async def is_liked(cls, tweet_id: int, user_id: int) -> bool:
        async with async_session_maker() as session:
            query = select(Like).where(
                Like.tweet_id == tweet_id, Like.user_id == user_id
            )
            res = await session.execute(query)
            return res.scalar_one_or_none() is not None
