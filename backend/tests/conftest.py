import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def auth_client(client):
    await client.post("/api/auth/send-code", json={"phone": "13800000000"})
    res = await client.post("/api/auth/login", json={"phone": "13800000000", "code": "123456"})
    token = res.json()["token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client
