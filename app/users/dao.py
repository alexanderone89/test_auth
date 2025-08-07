from dataclasses import dataclass

from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import UserNotFoundException
from app.users.models import User


@dataclass
class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def delete_user(cls, user_id: int):
        query = select(User).filter_by(id=user_id)
        async with async_session_maker() as session:
            user = (await session.execute(query)).scalar_one_or_none()
            user.is_active = False
            await session.commit()
            await session.flush()

            return user

    @classmethod
    async def full_delete(cls, user_id: int)->None:
        user = await cls.find_one_or_none_by_id(user_id)
        if not user:
            raise UserNotFoundException
        query = delete(User).where(user_id == User.id)
        async with async_session_maker() as session:
            await session.execute(query)
            await session.commit()
