import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import ProposalResult
from app.schemas.proposal_schema import ProposalInput, ProposalOutput
from app.services.proposal_service import generate_b2b_proposal
from app.validators.proposal_validator import validate_proposal_output

router = APIRouter()


@router.post(
    "/generate-proposal",
    response_model=ProposalOutput,
    tags=["Module 2: AI B2B Proposal Generator"],
)
def proposal_generator(data: ProposalInput, db: Session = Depends(get_db)):

    try:
        result = generate_b2b_proposal(data)
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

    validate_proposal_output(parsed_json, data.budget)

    # store result in database
    db_record = ProposalResult(
        client_type=data.client_type,
        budget=data.budget,
        employee_count=data.employee_count,
        sustainability_goal=data.sustainability_goal,
        product_mix=json.dumps(parsed_json["product_mix"]),
        budget_allocation=json.dumps(parsed_json["budget_allocation"]),
        impact_summary=parsed_json["impact_summary"],
    )
    db.add(db_record)
    db.commit()

    return parsed_json


@router.get(
    "/history/proposals",
    tags=["Module 2: AI B2B Proposal Generator"],
    summary="Retrieve past proposal generation results",
)
def get_proposal_history(limit: int = 20, db: Session = Depends(get_db)):
    records = (
        db.query(ProposalResult)
        .order_by(ProposalResult.created_at.desc())
        .limit(limit)
        .all()
    )
    return {"count": len(records), "results": [r.to_dict() for r in records]}