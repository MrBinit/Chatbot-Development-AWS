# tests/conftest.py
import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

os.environ.setdefault("OPENSEARCH_COLLECTION_ENDPOINT", "http://localhost")
os.environ.setdefault("Access_Key", "test")
os.environ.setdefault("Secret_Access_Key", "test")
os.environ.setdefault("AUTH_SECRET_KEY", "admin123")

from app.main import app
from app.api.v1.rag import get_rag_service

# Async test client
@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client

# Mock RAG service
@pytest.fixture
def override_rag_service():
    class MockRAGService:
        async def answer(self, query: str, top_k: int = 5):
            return "This is a mocked answer"

    app.dependency_overrides[get_rag_service] = lambda: MockRAGService()
    yield
    app.dependency_overrides.clear()
