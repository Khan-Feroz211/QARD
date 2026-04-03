"""Academic service: fetch and sync student records from the university LMS API."""

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AcademicRecord, CourseResult, Tenant, User
from app.models.schemas import AcademicResponse, CourseResultSchema


async def get_current_record(db: AsyncSession, user: User) -> AcademicResponse:
    """Return the most recent academic record for the student."""
    result = await db.execute(
        select(AcademicRecord)
        .where(AcademicRecord.user_id == user.id)
        .order_by(AcademicRecord.synced_at.desc())
    )
    record = result.scalar_one_or_none()
    if record is None:
        return AcademicResponse(
            semester="N/A",
            year=0,
            gpa=None,
            cgpa=None,
            program=None,
            department=None,
            status="enrolled",
            courses=[],
        )
    courses = await _get_courses(db, record.id)
    return _to_response(record, courses)


async def get_all_records(db: AsyncSession, user: User) -> list[AcademicResponse]:
    """Return all academic records for the student."""
    result = await db.execute(
        select(AcademicRecord)
        .where(AcademicRecord.user_id == user.id)
        .order_by(AcademicRecord.year.desc(), AcademicRecord.semester.desc())
    )
    records = result.scalars().all()
    responses = []
    for rec in records:
        courses = await _get_courses(db, rec.id)
        responses.append(_to_response(rec, courses))
    return responses


async def sync_from_lms(db: AsyncSession, user: User) -> None:
    """Fetch academic data from the university LMS API and persist it."""
    tenant_result = await db.execute(
        select(Tenant).where(Tenant.id == user.tenant_id)
    )
    tenant = tenant_result.scalar_one_or_none()
    if tenant is None or not tenant.lms_api_url:
        return

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{tenant.lms_api_url}/students/{user.student_id}/academic",
                headers={"Authorization": f"Bearer {tenant.lms_api_key}"},
            )
            response.raise_for_status()
            data = response.json()
    except Exception:
        return

    record = AcademicRecord(
        user_id=user.id,
        semester=data.get("semester", "Unknown"),
        year=data.get("year", 0),
        gpa=data.get("gpa"),
        cgpa=data.get("cgpa"),
        program=data.get("program"),
        department=data.get("department"),
        status=data.get("status", "enrolled"),
    )
    db.add(record)
    await db.flush()

    for course in data.get("courses", []):
        db.add(
            CourseResult(
                academic_record_id=record.id,
                course_code=course.get("code", ""),
                course_name=course.get("name", ""),
                credits=course.get("credits", 0),
                grade=course.get("grade"),
                marks_obtained=course.get("marks_obtained"),
                max_marks=course.get("max_marks"),
            )
        )
    await db.commit()


async def _get_courses(db: AsyncSession, record_id: str) -> list[CourseResultSchema]:
    result = await db.execute(
        select(CourseResult).where(CourseResult.academic_record_id == record_id)
    )
    rows = result.scalars().all()
    return [
        CourseResultSchema(
            course_code=r.course_code,
            course_name=r.course_name,
            credits=r.credits,
            grade=r.grade,
            marks_obtained=r.marks_obtained,
            max_marks=r.max_marks,
        )
        for r in rows
    ]


def _to_response(record: AcademicRecord, courses: list) -> AcademicResponse:
    return AcademicResponse(
        semester=record.semester,
        year=record.year,
        gpa=record.gpa,
        cgpa=record.cgpa,
        program=record.program,
        department=record.department,
        status=record.status,
        courses=courses,
    )
