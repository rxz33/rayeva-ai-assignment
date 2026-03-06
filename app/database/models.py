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
    seo_tags = Column(Text, nullable=False)
    sustainability_filters = Column(Text, nullable=False)
    sustainability_score = Column(Integer, nullable=True)
    score_reasoning = Column(Text, nullable=True)
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
            "sustainability_score": self.sustainability_score,
            "score_reasoning": self.score_reasoning,
            "created_at": self.created_at.isoformat(),
        }


class ProposalResult(Base):
    __tablename__ = "proposal_results"

    id = Column(Integer, primary_key=True, index=True)
    client_type = Column(String, nullable=False)
    budget = Column(Integer, nullable=False)
    employee_count = Column(Integer, nullable=False)
    sustainability_goal = Column(Text, nullable=False)
    product_mix = Column(Text, nullable=False)
    budget_allocation = Column(Text, nullable=False)
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


class ImpactReport(Base):
    __tablename__ = "impact_reports"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, nullable=False, index=True)
    plastic_saved_kg = Column(Float, nullable=False)
    carbon_avoided_kg = Column(Float, nullable=False)
    local_sourcing_summary = Column(Text, nullable=False)
    impact_statement = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "plastic_saved_kg": self.plastic_saved_kg,
            "carbon_avoided_kg": self.carbon_avoided_kg,
            "local_sourcing_summary": self.local_sourcing_summary,
            "impact_statement": self.impact_statement,
            "created_at": self.created_at.isoformat(),
        }


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
