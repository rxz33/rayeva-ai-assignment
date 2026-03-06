from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import CategoryResult, ImpactReport, ProposalResult

router = APIRouter()


@router.get("/stats", summary="Platform-wide AI usage statistics")
def get_stats(db: Session = Depends(get_db)):

    total_categories = db.query(func.count(CategoryResult.id)).scalar() or 0
    total_proposals = db.query(func.count(ProposalResult.id)).scalar() or 0
    total_impact_reports = db.query(func.count(ImpactReport.id)).scalar() or 0

    total_budget = db.query(func.sum(ProposalResult.budget)).scalar() or 0

    avg_score = db.query(func.avg(CategoryResult.sustainability_score)).scalar()
    avg_score = round(avg_score, 1) if avg_score else None

    most_common_category = (
        db.query(CategoryResult.primary_category, func.count(CategoryResult.primary_category).label("cnt"))
        .group_by(CategoryResult.primary_category)
        .order_by(func.count(CategoryResult.primary_category).desc())
        .first()
    )

    total_plastic_saved = db.query(func.sum(ImpactReport.plastic_saved_kg)).scalar() or 0
    total_carbon_avoided = db.query(func.sum(ImpactReport.carbon_avoided_kg)).scalar() or 0

    return {
        "categories": {
            "total": total_categories,
            "avg_sustainability_score": avg_score,
            "most_common_category": most_common_category[0] if most_common_category else None,
        },
        "proposals": {
            "total": total_proposals,
            "total_budget_proposed_inr": total_budget,
        },
        "impact_reports": {
            "total": total_impact_reports,
            "total_plastic_saved_kg": round(total_plastic_saved, 2),
            "total_carbon_avoided_kg": round(total_carbon_avoided, 2),
        },
    }