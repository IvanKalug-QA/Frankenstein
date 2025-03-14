import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.base import Base
from app.core.db import get_async_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(bind=test_engine, class_=AsyncSession,
                                   expire_on_commit=False)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setub_test_db():
    """Создаем асинхронную БД."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def async_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture()
async def test_app(async_session: AsyncSession):
    async def override_get_db():
        yield async_session
    app.dependency_overrides[get_async_session] = override_get_db
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope='session')
async def async_client():
    async with AsyncClient(
         transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac
