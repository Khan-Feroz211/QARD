"""Academic router: semester data, GPA, results, and LMS sync."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.dependencies import get_current_user, get_db
from app.models.schemas import AcademicResponse
from app.services import academic as academic_service

router = APIRouter()


@router.get("", response_model=AcademicResponse)
async def get_current_academic(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AcademicResponse:
    """Return the student's most recent semester and GPA."""
    return await academic_service.get_current_record(db, current_user)


@router.get("/history", response_model=list[AcademicResponse])
async def get_academic_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[AcademicResponse]:
    """Return all past academic records for the student."""
    return await academic_service.get_all_records(db, current_user)


@router.post("/sync")
async def sync_academic(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Trigger a manual sync from the university LMS API."""
    await academic_service.sync_from_lms(db, current_user)
    return {"message": "Sync triggered"}
