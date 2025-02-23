from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User


async def get_user(username: str, session: AsyncSession) -> User | None:
    user = await session.execute(select(User).where(User.username == username))
    return user.scalars().first()


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    user = await session.execute(select(User).where(User.id == user_id))
    return user.scalars().first()
