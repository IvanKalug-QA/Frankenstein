import pytest

from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session


@pytest.mark.asyncio
async def test_base(async_client: AsyncClient):
    response = await async_client.get('/users/me')
    print(response)


@pytest.mark.asyncio
async def test_register_user(
        async_client: AsyncClient,
        session: AsyncSession = Depends(get_async_session)):
    response = await async_client.get('/users')