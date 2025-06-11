from sqlalchemy import select
from app.user.models import User
from app.database import async_session_maker
from app.dao.base import BaseDao

class UserDAO(BaseDao):
    model = User

    @classmethod
    async def find_by_api_key(cls, api_key: str):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.api_key == api_key)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, name: str, api_key: str):
        async with async_session_maker() as session:
            user = User(name=name, api_key=api_key)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user