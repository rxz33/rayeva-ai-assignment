from typing import List

from pydantic import BaseModel


class ProductInput(BaseModel):
    product_name: str
    description: str
    material: str
    use_case: str


class CategoryOutput(BaseModel):
    primary_category: str
    sub_category: str
    seo_tags: List[str]
    sustainability_filters: List[str]

    class Config:
        schema_extra = {
            "example": {
                "primary_category": "personal_care",
                "sub_category": "oral_care",
                "seo_tags": ["bamboo", "eco friendly", "sustainable", "oral care"],
                "sustainability_filters": [
                    "biodegradable",
                    "renewable resources",
                    "plastic free",
                ],
            }
        }
