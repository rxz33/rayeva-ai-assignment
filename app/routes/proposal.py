import json

from fastapi import APIRouter, HTTPException, status

from app.schemas.proposal_schema import ProposalInput, ProposalOutput
from app.services.proposal_service import generate_b2b_proposal
from app.validators.proposal_validator import validate_proposal_output

router = APIRouter()


@router.post(
    "/generate-proposal",
    response_model=ProposalOutput,
    tags=["Module 2: AI B2B Proposal Generator"],
)
def proposal_generator(data: ProposalInput):

    try:
        result = generate_b2b_proposal(data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI service failed: {str(e)}",
        )

    result = result.replace("```json", "").replace("```", "")

    try:
        parsed_json = json.loads(result)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI returned invalid JSON format",
        )

    validate_proposal_output(parsed_json, data.budget)

    return parsed_json
