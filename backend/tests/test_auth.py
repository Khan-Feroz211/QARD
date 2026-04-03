"""Tests for authentication endpoints: register, login, and OTP flows."""

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_register_unknown_university():
    """Registering with an unknown university slug should return 400."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "Ali Khan",
                "email": "ali@test.com",
                "phone": "+923001234567",
                "student_id": "F21-0001",
                "password": "securepass123",
                "university_slug": "unknown-uni",
            },
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """Login with invalid credentials should return 401."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "nobody@test.com",
                "password": "wrongpassword",
                "university_slug": "nust",
            },
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_send_otp_returns_200():
    """Sending an OTP to a valid phone number should return 200."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/otp/send",
            params={"phone": "+923001234567"},
        )
    assert response.status_code == 200
    assert response.json()["message"] == "OTP sent"


@pytest.mark.asyncio
async def test_verify_otp_invalid():
    """Verifying an incorrect OTP should return 400."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/otp/verify",
            json={"phone": "+923001234567", "otp_code": "000000"},
        )
    assert response.status_code == 400
