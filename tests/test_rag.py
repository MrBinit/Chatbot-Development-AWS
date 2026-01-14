# tests/test_rag.py
import pytest


@pytest.mark.asyncio
async def test_rag_requires_auth(async_client):
    resp = await async_client.post(
        "/rag/answer",
        json={"query": "What is AI?"},
    )

    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_rag_with_auth(async_client, override_rag_service):
    # Login
    login = await async_client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    token = login.json()["access_token"]

    # Call RAG
    resp = await async_client.post(
        "/rag/answer",
        headers={"Authorization": f"Bearer {token}"},
        json={"query": "What is the National AI Policy?"},
    )

    assert resp.status_code == 200
    assert resp.json()["answer"] == "This is a mocked answer"
