from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer

from app.core.config import settings

access_security = JwtAccessBearer(secret_key=settings.secret, auto_error=True)
refresh_security = JwtRefreshBearer(secret_key=settings.secret)
