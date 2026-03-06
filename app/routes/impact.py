import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import ImpactReport
from app.schemas.impact_schema import ImpactInput, ImpactOutput
from app.services.impact_service import generate_impact_report
from app.validators.impact_validator import validate_impact_output

router = APIRouter()


@router.post(
    "/generate-impact-report",
    response_model=ImpactOutput,
    tags=["Module 3: AI Impact Reporting Generator"],
)
def impact_generator(data: ImpactInput, db: Session = Depends(get_db)):

    try:
        result = generate_impact_report(data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI service failed: {str(e)}",
        )

    try:
        parsed_json = json.loads(result)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI returned invalid JSON: {str(e)}",
        )

    validate_impact_output(parsed_json)

    db_record = ImpactReport(
        order_id=parsed_json["order_id"],
        plastic_saved_kg=parsed_json["plastic_saved_kg"],
        carbon_avoided_kg=parsed_json["carbon_avoided_kg"],
        local_sourcing_summary=parsed_json["local_sourcing_summary"],
        impact_statement=parsed_json["impact_statement"],
    )
    db.add(db_record)
    db.commit()

    return parsed_json


@router.get(
    "/history/impact-reports",
    tags=["Module 3: AI Impact Reporting Generator"],
    summary="Retrieve past impact reports",
)
def get_impact_history(limit: int = 20, db: Session = Depends(get_db)):
    records = (
        db.query(ImpactReport)
        .order_by(ImpactReport.created_at.desc())
        .limit(limit)
        .all()
    )
    return {"count": len(records), "results": [r.to_dict() for r in records]}
