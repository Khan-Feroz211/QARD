"""Usage router: usage event history and alert management."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.dependencies import get_current_user, get_db
from app.models.schemas import AlertResponse, UsageEventResponse
from app.services import usage as usage_service

router = APIRouter()


@router.get("/usage", response_model=list[UsageEventResponse])
async def get_usage_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[UsageEventResponse]:
    """Return the student's card usage event history."""
    return await usage_service.get_usage_history(db, current_user)


@router.get("/alerts", response_model=list[AlertResponse])
async def get_alerts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[AlertResponse]:
    """Return unread alerts for the current student."""
    return await usage_service.get_unread_alerts(db, current_user)


@router.put("/alerts/{alert_id}/read")
async def mark_alert_read(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Mark a specific alert as read."""
    await usage_service.mark_alert_read(db, current_user, alert_id)
    return {"message": "Alert marked as read"}
