import pytest


@pytest.mark.asyncio
async def test_send_code(client):
    res = await client.post("/api/auth/send-code", json={"phone": "13800000001"})
    assert res.status_code == 200
    assert res.json()["message"] == "验证码已发送"


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/api/auth/send-code", json={"phone": "13800000002"})
    res = await client.post("/api/auth/login", json={"phone": "13800000002", "code": "123456"})
    assert res.status_code == 200
    data = res.json()
    assert "token" in data
    assert "user_id" in data


@pytest.mark.asyncio
async def test_login_wrong_code(client):
    await client.post("/api/auth/send-code", json={"phone": "13800000003"})
    res = await client.post("/api/auth/login", json={"phone": "13800000003", "code": "000000"})
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_health(client):
    res = await client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
