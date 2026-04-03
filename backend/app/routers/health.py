"""Health router: liveness and readiness probe endpoint."""

import time
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db

router = APIRouter()

_START_TIME = time.time()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)) -> dict:
    """Return application health status, uptime, and version."""
    try:
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    uptime_seconds = int(time.time() - _START_TIME)
    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime_seconds": uptime_seconds,
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
