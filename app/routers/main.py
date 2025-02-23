from fastapi import APIRouter

from app.api.endpoints.users import users_router

main_router = APIRouter()

main_router.include_router(users_router)
