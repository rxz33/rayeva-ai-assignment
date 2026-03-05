import json
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from app.database.db import Base


class CategoryResult(Base):
    __tablename__ = "category_results"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    material = Column(String, nullable=False)
    use_case = Column(String, nullable=False)
    primary_category = Column(String, nullable=False)
    sub_category = Column(String, nullable=False)
    seo_tags = Column(Text, nullable=False)           # stored as JSON string
    sustainability_filters = Column(Text, nullable=False)  # stored as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "description": self.description,   
            "material": self.material,         
            "use_case": self.use_case,          
            "primary_category": self.primary_category,
            "sub_category": self.sub_category,
            "seo_tags": json.loads(self.seo_tags),
            "sustainability_filters": json.loads(self.sustainability_filters),
            "created_at": self.created_at.isoformat(),
        }


class ProposalResult(Base):
    __tablename__ = "proposal_results"

    id = Column(Integer, primary_key=True, index=True)
    client_type = Column(String, nullable=False)
    budget = Column(Integer, nullable=False)
    employee_count = Column(Integer, nullable=False)
    sustainability_goal = Column(Text, nullable=False)
    product_mix = Column(Text, nullable=False)        # stored as JSON string
    budget_allocation = Column(Text, nullable=False)  # stored as JSON string
    impact_summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "client_type": self.client_type,
            "budget": self.budget,
            "employee_count": self.employee_count,
            "sustainability_goal": self.sustainability_goal,
            "product_mix": json.loads(self.product_mix),
            "budget_allocation": json.loads(self.budget_allocation),
            "impact_summary": self.impact_summary,
            "created_at": self.created_at.isoformat(),
        }