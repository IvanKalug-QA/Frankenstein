from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.utils import access_security, refresh_security
from app.core.user import get_user_manager
from app.models.user import User
from fastapi_users.manager import BaseUserManager
from http import HTTPStatus

users_router = APIRouter()


@users_router.post("/auth/jwt/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_manager: BaseUserManager = Depends(get_user_manager)
):
    """Аутентификация токенов"""
    user = user_manager.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid login or password!")
    access_token = access_security.create_access_token(subject=str(user.id))
    refresh_token = refresh_security.create_refresh_token(subject=str(user.id))
    return {"acess_token": access_token, "refresh_token": refresh_token}


@users_router.post("/auth/jwt/refresh")
async def refresh(
    token_data: dict = Depends(refresh_security)
):
    new_access = access_security.create_access_token(subject=token_data.get("sub"))
    new_refresh = refresh_security.create_refresh_token(subject=token_data.get("sub"))
    return {"acess_token": new_access, "refresh_token": new_refresh}
