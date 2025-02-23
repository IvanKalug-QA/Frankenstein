from typing import Union
from http import HTTPStatus
import jwt
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.authentication import BearerTransport, Strategy, AuthenticationBackend
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from app.core.db import get_async_session
from app.models.user import User
from app.schemas.users import UserCreate

from app.core.config import settings


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(self, password: str, user: Union[UserCreate, User]) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(reason='Password should be at least 3 characters')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.secret, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


class JWTStrategy(Strategy[User, int]):
    def __init__(self):
        pass

    async def read_token(self, token: str, user_manager) -> Optional[User]:
        """Читает токен и возвращает пользователя, если токен валиден"""
        try:
            payload = jwt.decode(token, settings.secret, algorithms=[settings.algorithm])
            user_id = int(payload.get("sub"))
            if not user_id:
                return None
            return await user_manager.get(user_id)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Access token expired")
        except jwt.PyJWTError:
            return None

    async def write_token(self, user: User) -> str:
        """Создаёт access токен"""
        expire = datetime.utcnow() + timedelta(minutes=15)
        payload = {"sub": str(user.id), "exp": expire}
        return jwt.encode(payload, settings.secret, algorithm=settings.algorithm)


bearer_transport = BearerTransport(tokenUrl="auth/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy()


jwt_auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
fastapi_users = FastAPIUsers(
    get_user_manager,
    [jwt_auth_backend]
)
