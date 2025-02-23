import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_base(async_client: AsyncClient):
    response = await async_client.get('/users/me')
    print(response)
