from typing import List
from pydantic import BaseModel, ConfigDict


class ProposalInput(BaseModel):
    client_type: str
    budget: int
    employee_count: int
    sustainability_goal: str


class ProductMix(BaseModel):
    product: str
    quantity: int
    unit_price: float
    total_cost: float


class BudgetAllocation(BaseModel):
    products: int
    logistics: int
    buffer: int


class ProposalOutput(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {}})
    product_mix: List[ProductMix]
    budget_allocation: BudgetAllocation
    impact_summary: str