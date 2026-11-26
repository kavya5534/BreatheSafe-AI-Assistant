from fastapi import APIRouter, HTTPException, Query

from app.database.repository import (
    create_community_report,
    create_sustainable_activity,
    list_community_reports,
    list_sustainable_activities,
    upvote_community_report,
)
from app.schemas import (
    CommunityReportCreate,
    CommunityReportOut,
    SustainableActivityCreate,
    SustainableActivityOut,
)

router = APIRouter(prefix="/api", tags=["reports"])


@router.get("/reports", response_model=list[CommunityReportOut])
def get_reports(limit: int = Query(default=50, ge=1, le=100)) -> list[CommunityReportOut]:
    records = list_community_reports(limit=limit)
    return [
        CommunityReportOut(
            id=rec.id or 0,
            reporter_name=rec.reporter_name,
            location=rec.location,
            latitude=rec.latitude,
            longitude=rec.longitude,
            category=rec.category,
            severity=rec.severity,
            description=rec.description,
            upvotes=rec.upvotes,
            is_sample=rec.is_sample,
            created_at=rec.created_at,
        )
        for rec in records
    ]


@router.post("/reports", response_model=CommunityReportOut, status_code=201)
def post_report(payload: CommunityReportCreate) -> CommunityReportOut:
    rec = create_community_report(payload)
    return CommunityReportOut(
        id=rec.id or 0,
        reporter_name=rec.reporter_name,
        location=rec.location,
        latitude=rec.latitude,
        longitude=rec.longitude,
        category=rec.category,
        severity=rec.severity,
        description=rec.description,
        upvotes=rec.upvotes,
        is_sample=rec.is_sample,
        created_at=rec.created_at,
    )


@router.post("/reports/{report_id}/upvote", response_model=CommunityReportOut)
def upvote_report(report_id: int) -> CommunityReportOut:
    rec = upvote_community_report(report_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Community report not found.")
    return CommunityReportOut(
        id=rec.id or 0,
        reporter_name=rec.reporter_name,
        location=rec.location,
        latitude=rec.latitude,
        longitude=rec.longitude,
        category=rec.category,
        severity=rec.severity,
        description=rec.description,
        upvotes=rec.upvotes,
        is_sample=rec.is_sample,
        created_at=rec.created_at,
    )


@router.get("/activities", response_model=list[SustainableActivityOut])
def get_activities(
    session_id: str = Query(default="default", min_length=1, max_length=64),
) -> list[SustainableActivityOut]:
    records = list_sustainable_activities(session_id=session_id)
    return [
        SustainableActivityOut(
            id=rec.id or 0,
            session_id=rec.session_id,
            activity_type=rec.activity_type,
            description=rec.description,
            co2_saved_kg=rec.co2_saved_kg,
            points=rec.points,
            created_at=rec.created_at,
        )
        for rec in records
    ]


@router.post("/activities", response_model=SustainableActivityOut, status_code=201)
def post_activity(payload: SustainableActivityCreate) -> SustainableActivityOut:
    rec = create_sustainable_activity(payload)
    return SustainableActivityOut(
        id=rec.id or 0,
        session_id=rec.session_id,
        activity_type=rec.activity_type,
        description=rec.description,
        co2_saved_kg=rec.co2_saved_kg,
        points=rec.points,
        created_at=rec.created_at,
    )
