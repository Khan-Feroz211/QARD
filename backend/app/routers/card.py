"""Card router: get, scan, and regenerate virtual student card."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.dependencies import get_current_user, get_db
from app.models.schemas import VirtualCardResponse
from app.services import card as card_service

router = APIRouter()


@router.get("", response_model=VirtualCardResponse)
async def get_card(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VirtualCardResponse:
    """Return the student's active virtual card."""
    return await card_service.get_active_card(db, current_user)


@router.post("/scan")
async def scan_card(
    merchant_name: str = "",
    location: str = "",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Log a card scan event."""
    await card_service.log_scan_event(db, current_user, merchant_name, location)
    return {"message": "Scan logged"}


@router.put("/regenerate", response_model=VirtualCardResponse)
async def regenerate_card(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VirtualCardResponse:
    """Invalidate the current card and issue a new card number."""
    return await card_service.regenerate_card(db, current_user)
