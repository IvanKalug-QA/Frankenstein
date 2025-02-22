from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserGet(schemas.BaseUser[int]):
    pass
