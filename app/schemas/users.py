from fastapi_users import schemas
from pydantic import BaseModel


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    username: str


class UserGet(schemas.BaseUser[int]):
    username: str


class TokenSchema(BaseModel):
    username: str
    password: str
