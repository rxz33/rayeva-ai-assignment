from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class ProductInput(BaseModel):
    product_name: str
    description: str
    material: str
    use_case: str


class CategoryOutput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "primary_category": "personal_care",
                "sub_category": "oral_care",
                "seo_tags": [
                    "bamboo",
                    "eco friendly",
                    "sustainable",
                    "plastic free",
                    "oral care",
                ],
                "sustainability_filters": [
                    "biodegradable",
                    "renewable resources",
                    "plastic free",
                ],
                "sustainability_score": 88,
                "score_reasoning": "Bamboo is a fast-growing renewable material that is fully biodegradable and replaces single-use plastic.",
            }
        }
    )

    primary_category: str
    sub_category: str
    seo_tags: List[str]
    sustainability_filters: List[str]
    sustainability_score: Optional[int] = None
    score_reasoning: Optional[str] = None

    @field_validator("seo_tags")
    @classmethod
    def validate_seo_tags_length(cls, v):
        if len(v) < 5 or len(v) > 10:
            raise ValueError("seo_tags must contain between 5 and 10 tags")
        return v
