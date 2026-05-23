import pytest


@pytest.mark.asyncio
async def test_create_garment(auth_client):
    res = await auth_client.post("/api/garments", json={"category": "tops", "image_url": "g/shirt.jpg"})
    assert res.status_code == 201
    assert res.json()["category"] == "tops"


@pytest.mark.asyncio
async def test_list_garments(auth_client):
    res = await auth_client.get("/api/garments")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


@pytest.mark.asyncio
async def test_get_garment(auth_client):
    create_res = await auth_client.post("/api/garments", json={"category": "pants", "image_url": "g/pants.jpg"})
    gid = create_res.json()["id"]

    res = await auth_client.get(f"/api/garments/{gid}")
    assert res.status_code == 200
    assert res.json()["category"] == "pants"
