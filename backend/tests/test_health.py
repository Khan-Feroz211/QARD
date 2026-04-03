"""Tests for the /health endpoint."""

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health_returns_200():
    """Health endpoint should return 200 with status ok."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body
    assert "uptime_seconds" in body


@pytest.mark.asyncio
async def test_health_contains_database_key():
    """Health response must include a 'database' key."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert "database" in response.json()
