import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """A test client with fresh seed data for every test."""
    with TestClient(app) as c:
        c.post("/api/test/reset")
        yield c
