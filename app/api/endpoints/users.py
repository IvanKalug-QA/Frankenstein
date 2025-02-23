from http import HTTPStatus
import jwt

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.manager import BaseUserManager

from fastapi.security import OAuth2PasswordRequestForm
from app.utils.users import create_access_token, create_refresh_token
from app.core.user import fastapi_users, get_user_manager, jwt_auth_backend
from app.schemas.users import UserCreate, UserGet, UserUpdate
from app.core.db import get_async_session
from app.database.users import get_user
from app.core.config import settings

users_router = APIRouter()


@users_router.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
    user_manager: BaseUserManager = Depends(get_user_manager),
):
    """Эндпоинт для логина пользователя и выдачи токенов."""
    user = await get_user(form_data.username, session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


@users_router.post("/auth/refresh")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.secret, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return {
            "access_token": create_access_token(user_id),
            "refresh_token": create_refresh_token(user_id),
            "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

users_router.include_router(
    fastapi_users.get_register_router(UserGet, UserCreate),
    prefix='/auth',
    tags=['auth']
)
users_router.include_router(
    fastapi_users.get_users_router(UserGet, UserUpdate),
    prefix='/users',
    tags=['users']
)

users_router.include_router(
    fastapi_users.get_auth_router(jwt_auth_backend),
    prefix="/auth",
    tags=["auth"],
)
