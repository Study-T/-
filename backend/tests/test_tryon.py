import pytest


@pytest.mark.asyncio
async def test_create_tryon(auth_client):
    g = await auth_client.post("/api/garments", json={"category": "tops", "image_url": "g/s.jpg"})
    garment_id = g.json()["id"]

    a = await auth_client.post("/api/avatars", json={"photo_url": "p/test.jpg"})
    avatar_id = a.json()["id"]

    res = await auth_client.post("/api/tryon", json={"avatar_id": avatar_id, "garment_id": garment_id})
    assert res.status_code == 201


@pytest.mark.asyncio
async def test_tryon_no_avatar(auth_client):
    res = await auth_client.post("/api/tryon", json={"avatar_id": 99999, "garment_id": 1})
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_tryon_history(auth_client):
    res = await auth_client.get("/api/tryon")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
