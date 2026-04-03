"""Admin service: student listing, benefit management, analytics, and tenant ops."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Benefit, Tenant, UsageEvent, User
from app.models.schemas import BenefitResponse, TenantCreateRequest


async def list_students(db: AsyncSession, tenant_id: str) -> list[dict]:
    """Return a summary list of all students for the given tenant."""
    result = await db.execute(
        select(User)
        .where(User.tenant_id == tenant_id, User.role == "student")
        .order_by(User.full_name)
    )
    users = result.scalars().all()
    return [
        {
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "student_id": u.student_id,
            "is_active": u.is_active,
            "is_verified": u.is_verified,
            "plan": u.plan,
        }
        for u in users
    ]


async def create_benefit(
    db: AsyncSession, tenant_id: str, payload: BenefitResponse
) -> Benefit:
    """Create a new university-specific benefit."""
    benefit = Benefit(
        tenant_id=tenant_id,
        title=payload.title,
        partner_name=payload.partner_name,
        discount_percent=payload.discount_percent,
        category=payload.category,
        logo_url=payload.logo_url,
        valid_until=payload.valid_until,
    )
    db.add(benefit)
    await db.commit()
    await db.refresh(benefit)
    return benefit


async def get_analytics(db: AsyncSession, tenant_id: str) -> dict:
    """Return aggregated usage analytics for the tenant."""
    student_count_result = await db.execute(
        select(func.count(User.id)).where(
            User.tenant_id == tenant_id, User.role == "student"
        )
    )
    student_count = student_count_result.scalar_one()

    event_count_result = await db.execute(
        select(func.count(UsageEvent.id))
        .join(User, User.id == UsageEvent.user_id)
        .where(User.tenant_id == tenant_id)
    )
    event_count = event_count_result.scalar_one()

    return {
        "total_students": student_count,
        "total_usage_events": event_count,
    }


async def update_branding(
    db: AsyncSession,
    tenant_id: str,
    primary_color: str,
    logo_url: str,
) -> None:
    """Update the tenant's primary color and logo URL."""
    result = await db.execute(select(Tenant).where(Tenant.id == tenant_id))
    tenant = result.scalar_one_or_none()
    if tenant:
        if primary_color:
            tenant.primary_color = primary_color
        if logo_url:
            tenant.logo_url = logo_url
        await db.commit()


async def create_tenant(db: AsyncSession, payload: TenantCreateRequest) -> Tenant:
    """Create and persist a new university tenant."""
    tenant = Tenant(
        slug=payload.slug,
        name=payload.name,
        plan=payload.plan,
        primary_color=payload.primary_color,
        lms_api_url=payload.lms_api_url,
    )
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)
    return tenant


async def list_tenants(db: AsyncSession) -> list[dict]:
    """Return all tenants for the super-admin view."""
    result = await db.execute(select(Tenant).order_by(Tenant.name))
    tenants = result.scalars().all()
    return [
        {
            "id": t.id,
            "slug": t.slug,
            "name": t.name,
            "plan": t.plan,
            "is_active": t.is_active,
            "created_at": t.created_at.isoformat(),
        }
        for t in tenants
    ]


async def update_tenant_plan(db: AsyncSession, tenant_id: str, plan: str) -> None:
    """Update the plan for the specified tenant."""
    result = await db.execute(select(Tenant).where(Tenant.id == tenant_id))
    tenant = result.scalar_one_or_none()
    if tenant:
        tenant.plan = plan
        await db.commit()
