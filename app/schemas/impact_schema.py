from typing import List

from pydantic import BaseModel, ConfigDict


class ImpactProduct(BaseModel):
    product_name: str
    quantity: int
    material: str


class ImpactInput(BaseModel):
    order_id: str
    products: List[ImpactProduct]


class ImpactOutput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "order_id": "ORD-1023",
                "plastic_saved_kg": 12.4,
                "carbon_avoided_kg": 8.2,
                "local_sourcing_summary": "60% of products sourced within 500km",
                "impact_statement": "This order prevented 12.4kg of plastic from entering landfill and avoided 8.2kg of CO2 equivalent emissions.",
            }
        }
    )

    order_id: str
    plastic_saved_kg: float
    carbon_avoided_kg: float
    local_sourcing_summary: str
    impact_statement: str