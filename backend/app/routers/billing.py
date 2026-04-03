"""Billing router: plan upgrade, Stripe webhooks, and billing status."""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.dependencies import get_current_user, get_db
from app.models.schemas import PlanUpgradeRequest
from app.services import billing as billing_service

router = APIRouter()


@router.post("/upgrade")
async def upgrade_plan(
    payload: PlanUpgradeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Initiate a Stripe Checkout session to upgrade the user to Pro."""
    checkout_url = await billing_service.create_checkout_session(db, current_user, payload)
    return {"checkout_url": checkout_url}


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)) -> dict:
    """Handle incoming Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    await billing_service.handle_stripe_webhook(db, payload, sig_header)
    return {"received": True}


@router.get("/status")
async def billing_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Return the current plan and renewal date for the user."""
    return await billing_service.get_billing_status(db, current_user)
