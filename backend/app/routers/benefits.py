"""Benefits router: list benefits and claim a benefit."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.dependencies import get_current_user, get_db
from app.models.schemas import BenefitResponse
from app.services import benefits as benefits_service

router = APIRouter()


@router.get("", response_model=list[BenefitResponse])
async def list_benefits(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[BenefitResponse]:
    """Return the benefits catalog filtered by the user's tenant."""
    return await benefits_service.get_benefits_for_tenant(db, current_user.tenant_id)


@router.post("/{benefit_id}/claim")
async def claim_benefit(
    benefit_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Log a benefit claim event for the given benefit."""
    await benefits_service.claim_benefit(db, current_user, benefit_id)
    return {"message": "Benefit claimed"}
