import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import CategoryResult
from app.schemas.category_schema import CategoryOutput, ProductInput
from app.services.category_service import generate_category_tags
from app.validators.category_validator import validate_category_output

router = APIRouter()


@router.post(
    "/generate-category",
    response_model=CategoryOutput,
    tags=["Module 1: AI Auto-Category & Tag Generator"],
)
def category_generator(product: ProductInput, db: Session = Depends(get_db)):
    try:
        result = generate_category_tags(product)
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

    validate_category_output(parsed_json)

    db_record = CategoryResult(
        product_name=product.product_name,
        description=product.description,
        material=product.material,
        use_case=product.use_case,
        primary_category=parsed_json["primary_category"],
        sub_category=parsed_json["sub_category"],
        seo_tags=json.dumps(parsed_json["seo_tags"]),
        sustainability_filters=json.dumps(parsed_json["sustainability_filters"]),
        sustainability_score=parsed_json.get("sustainability_score"),
        score_reasoning=parsed_json.get("score_reasoning"),
    )
    db.add(db_record)
    db.commit()
    return parsed_json


@router.get("/history/categories", tags=["Module 1: AI Auto-Category & Tag Generator"])
def get_category_history(
    limit: int = 20, category: str = None, db: Session = Depends(get_db)
):
    query = db.query(CategoryResult)
    if category:
        query = query.filter(CategoryResult.primary_category == category)
    records = query.order_by(CategoryResult.created_at.desc()).limit(limit).all()
    return {"count": len(records), "results": [r.to_dict() for r in records]}
