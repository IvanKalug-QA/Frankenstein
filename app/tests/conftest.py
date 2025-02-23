import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest_asyncio.fixture(scope='session')
async def async_client():
    async with AsyncClient(
         transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac
