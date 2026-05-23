import pytest


@pytest.mark.asyncio
async def test_create_avatar(auth_client):
    res = await auth_client.post("/api/avatars", json={"photo_url": "photos/test.jpg"})
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "pending"
    assert data["photo_url"] == "photos/test.jpg"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_avatars(auth_client):
    res = await auth_client.get("/api/avatars")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


@pytest.mark.asyncio
async def test_get_avatar(auth_client):
    create_res = await auth_client.post("/api/avatars", json={"photo_url": "photos/test.jpg"})
    avatar_id = create_res.json()["id"]

    res = await auth_client.get(f"/api/avatars/{avatar_id}")
    assert res.status_code == 200
    assert res.json()["id"] == avatar_id


@pytest.mark.asyncio
async def test_get_avatar_not_found(auth_client):
    res = await auth_client.get("/api/avatars/99999")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_update_avatar_params(auth_client):
    create_res = await auth_client.post("/api/avatars", json={"photo_url": "photos/test.jpg"})
    avatar_id = create_res.json()["id"]

    res = await auth_client.put(f"/api/avatars/{avatar_id}/params", json={"waist": 0.8, "height": 1.75})
    assert res.status_code == 200
    assert res.json()["smplx_params"] == {"waist": 0.8, "height": 1.75}


@pytest.mark.asyncio
async def test_delete_avatar(auth_client):
    create_res = await auth_client.post("/api/avatars", json={"photo_url": "photos/test.jpg"})
    avatar_id = create_res.json()["id"]

    res = await auth_client.delete(f"/api/avatars/{avatar_id}")
    assert res.status_code == 204

    get_res = await auth_client.get(f"/api/avatars/{avatar_id}")
    assert get_res.status_code == 404


@pytest.mark.asyncio
async def test_max_3_avatars(auth_client):
    for i in range(3):
        res = await auth_client.post("/api/avatars", json={"photo_url": f"p/{i}.jpg"})
        assert res.status_code == 201

    res = await auth_client.post("/api/avatars", json={"photo_url": "p/4.jpg"})
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_require_auth(client):
    res = await client.post("/api/avatars", json={"photo_url": "test.jpg"})
    assert res.status_code == 401
