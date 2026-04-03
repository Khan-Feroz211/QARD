"""Tests for virtual card endpoints."""

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_get_card_unauthenticated():
    """Fetching the card without a token should return 401."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/card")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_scan_card_unauthenticated():
    """Scanning a card without a token should return 401."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/card/scan")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_regenerate_card_unauthenticated():
    """Regenerating a card without a token should return 401."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/v1/card/regenerate")
    assert response.status_code == 401
