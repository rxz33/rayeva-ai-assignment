import json

from fastapi import APIRouter, HTTPException, status

from app.schemas.category_schema import CategoryOutput, ProductInput
from app.services.category_service import generate_category_tags
from app.validators.category_validator import validate_category_output

router = APIRouter()


@router.post(
    "/generate-category",
    response_model=CategoryOutput,
    tags=["Module 1: AI Auto-Category & Tag Generator"],
)
def category_generator(product: ProductInput):

    try:
        result = generate_category_tags(product)
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

    validate_category_output(parsed_json)

    return parsed_json
