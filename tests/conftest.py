import asyncio
import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import Base, engine


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_db():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac