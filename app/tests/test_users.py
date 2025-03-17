import pytest

from httpx import AsyncClient

from app.schemas.users import UserCreate


@pytest.mark.asyncio
async def test_register_user(
        async_client: AsyncClient,
        get_user_schema: UserCreate):
    response = await async_client.post(
        '/auth/register', json=get_user_schema.dict())
    assert response.status_code == 201
    data = response.json()
    assert data['username'] == get_user_schema.username
    assert data['email'] == get_user_schema.email


@pytest.mark.asyncio
async def test_user_info(
        get_access_token: str,
        async_client: AsyncClient,
        get_user_schema: UserCreate):
    headers = {"Authorization": f"Bearer {get_access_token}"}
    response = await async_client.get('users/me', headers=headers)
    data = response.json()
    assert data['username'] == get_user_schema.username
    assert data['email'] == get_user_schema.email
