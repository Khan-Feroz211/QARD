"""Admin router: university admin and super-admin management endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.dependencies import get_db, require_role
from app.models.schemas import BenefitResponse, TenantCreateRequest
from app.services import admin as admin_service

router = APIRouter()


# ── University Admin ────────────────────────────────────────────────────────


@router.get("/admin/students")
async def list_students(
    current_user: User = Depends(require_role("admin", "superadmin")),
    db: AsyncSession = Depends(get_db),
) -> list:
    """List all students belonging to the admin's tenant."""
    return await admin_service.list_students(db, current_user.tenant_id)


@router.post("/admin/benefits", response_model=BenefitResponse)
async def create_benefit(
    payload: BenefitResponse,
    current_user: User = Depends(require_role("admin", "superadmin")),
    db: AsyncSession = Depends(get_db),
) -> BenefitResponse:
    """Create a university-specific benefit."""
    return await admin_service.create_benefit(db, current_user.tenant_id, payload)


@router.get("/admin/analytics")
async def get_analytics(
    current_user: User = Depends(require_role("admin", "superadmin")),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Return usage analytics dashboard data for the tenant."""
    return await admin_service.get_analytics(db, current_user.tenant_id)


@router.put("/admin/branding")
async def update_branding(
    primary_color: str = "",
    logo_url: str = "",
    current_user: User = Depends(require_role("admin", "superadmin")),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Update the university's branding (colors and logo)."""
    await admin_service.update_branding(db, current_user.tenant_id, primary_color, logo_url)
    return {"message": "Branding updated"}


# ── Super Admin ──────────────────────────────────────────────────────────────


@router.post("/superadmin/tenants")
async def create_tenant(
    payload: TenantCreateRequest,
    current_user: User = Depends(require_role("superadmin")),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Create a new university tenant."""
    tenant = await admin_service.create_tenant(db, payload)
    return {"id": tenant.id, "slug": tenant.slug}


@router.get("/superadmin/tenants")
async def list_tenants(
    current_user: User = Depends(require_role("superadmin")),
    db: AsyncSession = Depends(get_db),
) -> list:
    """List all university tenants."""
    return await admin_service.list_tenants(db)


@router.put("/superadmin/tenants/{tenant_id}/plan")
async def update_tenant_plan(
    tenant_id: str,
    plan: str,
    current_user: User = Depends(require_role("superadmin")),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Update the plan for a specific tenant."""
    await admin_service.update_tenant_plan(db, tenant_id, plan)
    return {"message": "Tenant plan updated"}
