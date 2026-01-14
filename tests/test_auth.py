import pytest

@pytest.mark.asyncio
async def test_login_success(async_client):
    resp = await async_client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_failure(async_client):
    resp = await async_client.post(
        "/auth/login",
        json={"username": "admin", "password": "wrong"},
    )

    assert resp.status_code == 401
