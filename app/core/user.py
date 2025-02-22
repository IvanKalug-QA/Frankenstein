from typing import Optional, Union
from http import HTTPStatus

from fastapi import Depends, Request, HTTPException
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.users import UserCreate
from app.utils.auth import access_security


async def get_user_db(session: AsyncSession=Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(self, password: str, user: Union[UserCreate, User]) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(reason='Password should be at least 3 characters')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


async def get_current_user(
    token_data: dict = Depends(access_security),
    user_managet: BaseUserManager = Depends(get_user_manager)
):
    user_id: int = int(token_data.get('sub'))
    user = await user_managet.get(user_id)
    if not user.is_active:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='User inactive'
        )
    return user

fastapi_users = FastAPIUsers(
    get_user_manager,
    [get_current_user]
)
