import jwt
from datetime import datetime, timedelta

from app.core.config import settings


def create_access_token(user_id: int):
    """Создаёт access-токен."""
    expire = datetime.utcnow() + timedelta(minutes=7)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.secret, algorithm=settings.algorithm)


def create_refresh_token(user_id: int):
    """Создаёт refresh-токен."""
    expire = datetime.utcnow() + timedelta(days=15)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.secret, algorithm=settings.algorithm)
