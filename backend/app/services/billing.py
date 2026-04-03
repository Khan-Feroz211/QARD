"""Billing service: Stripe and JazzCash payment integration."""

import stripe
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.models import User
from app.models.schemas import PlanUpgradeRequest

stripe.api_key = settings.STRIPE_SECRET_KEY


async def create_checkout_session(
    db: AsyncSession,
    user: User,
    payload: PlanUpgradeRequest,
) -> str:
    """Create a Stripe Checkout session and return the redirect URL."""
    if not user.stripe_customer_id:
        customer = stripe.Customer.create(
            email=user.email,
            name=user.full_name,
            metadata={"user_id": user.id, "tenant_id": user.tenant_id},
        )
        user.stripe_customer_id = customer.id
        await db.commit()

    session = stripe.checkout.Session.create(
        customer=user.stripe_customer_id,
        payment_method_types=["card"],
        line_items=[{"price": settings.STRIPE_PRO_PRICE_ID, "quantity": 1}],
        mode="subscription",
        success_url="https://app.qard.pk/billing/success",
        cancel_url="https://app.qard.pk/billing/cancel",
        metadata={"user_id": user.id},
    )
    return session.url


async def handle_stripe_webhook(
    db: AsyncSession, payload: bytes, sig_header: str
) -> None:
    """Validate and process a Stripe webhook event."""
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (stripe.error.SignatureVerificationError, ValueError):
        return

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("metadata", {}).get("user_id")
        if user_id:
            from sqlalchemy import select

            result = await db.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            if user:
                user.plan = "pro"
                await db.commit()


async def get_billing_status(db: AsyncSession, user: User) -> dict:
    """Return the user's current plan and Stripe subscription renewal date."""
    renewal_date = None
    if user.stripe_customer_id:
        try:
            subscriptions = stripe.Subscription.list(
                customer=user.stripe_customer_id, status="active", limit=1
            )
            if subscriptions.data:
                renewal_date = subscriptions.data[0].current_period_end
        except Exception:
            pass

    return {
        "plan": user.plan,
        "stripe_customer_id": user.stripe_customer_id,
        "renewal_date": renewal_date,
    }
