from sqlalchemy import select
from sqlalchemy.orm import selectinload,joinedload

from app.follower.models import Follower
from app.user.models import User
from app.database import async_session_maker
from app.dao.base import BaseDao

class UserDAO(BaseDao):
    model = User


    @classmethod
    async def get_user_by_api_key(cls, api_key: str):
        async with async_session_maker() as session:
            stmt = (
                select(User)
                .options(
                    joinedload(User.followers).joinedload(Follower.follower).load_only(User.id, User.name),
                    joinedload(User.following).joinedload(Follower.followed).load_only(User.id, User.name),
                )
                .where(User.api_key == api_key)
            )
            result = await session.execute(stmt)
            user = result.scalars().first()
            return user

    @classmethod
    async def get_user_by_user_id(user_id: int) -> User:
        async with async_session_maker() as session:
            stmt = (
                select(User)
                .where(User.id == user_id)
                .options(
                    joinedload(User.followers).joinedload(Follower.follower).load_only(User.id, User.name),
                    joinedload(User.following).joinedload(Follower.followed).load_only(User.id, User.name),
                )
            )
            result = await session.execute(stmt)
            return result.scalar_one()

    @classmethod
    async def create(cls, name: str, api_key: str):
        async with async_session_maker() as session:
            user = User(name=name, api_key=api_key)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @classmethod
    async def get_user_profile(cls, user_id: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(User)
                .options(
                    selectinload(User.followers).selectinload(Follower.follower),
                    selectinload(User.following).selectinload(Follower.followed),
                )
                .where(User.id == user_id)
            )
            return result.scalar_one_or_none()