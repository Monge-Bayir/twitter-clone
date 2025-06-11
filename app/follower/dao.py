from sqlalchemy import select, and_
from app.follower.models import Follower
from app.database import async_session_maker
from app.dao.base import BaseDao

class FollowerDAO(BaseDao):
    model = Follower

    @classmethod
    async def follow(cls, follower_id: int, followed_id: int):
        async with async_session_maker() as session:
            follow = Follower(follower_id=follower_id, followed_id=followed_id)
            session.add(follow)
            await session.commit()
            await session.refresh(follow)
            return follow

    @classmethod
    async def unfollow(cls, follower_id: int, followed_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(
                and_(
                    cls.model.follower_id == follower_id,
                    cls.model.followed_id == followed_id
                )
            )
            result = await session.execute(query)
            follow = result.scalar_one_or_none()
            if follow:
                await session.delete(follow)
                await session.commit()
                return True
            return False