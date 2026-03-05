from typing import List

from pydantic import BaseModel


class ProposalInput(BaseModel):
    client_type: str
    budget: int
    employee_count: int
    sustainability_goal: str


class ProductMix(BaseModel):
    product: str
    quantity: int


class BudgetAllocation(BaseModel):
    products: int
    logistics: int
    buffer: int


class ProposalOutput(BaseModel):
    product_mix: List[ProductMix]
    budget_allocation: BudgetAllocation
    impact_summary: str

    class Config:
        schema_extra = {
            "example": {
                "product_mix": [
                    {"product": "reusable steel water bottle", "quantity": 200},
                    {"product": "bamboo toothbrush", "quantity": 200},
                ],
                "budget_allocation": {
                    "products": 85000,
                    "logistics": 10000,
                    "buffer": 5000,
                },
                "impact_summary": "Reusable products reduce single-use plastic waste and encourage sustainable habits in the workplace.",
            }
        }
