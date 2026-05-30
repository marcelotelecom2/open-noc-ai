from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PolicyRuleBase(BaseModel):
    name: str = Field(..., max_length=255)
    scope: str = Field(..., max_length=100)
    effect: str = Field(..., max_length=50)
    action_type: str | None = Field(default=None, max_length=100)
    target_type: str | None = Field(default=None, max_length=100)
    conditions: dict | None = None
    description: str | None = None
    status: str = Field(default="active", max_length=50)


class PolicyRuleCreate(PolicyRuleBase):
    tenant_id: UUID


class PolicyRuleUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    effect: str | None = Field(default=None, max_length=50)
    conditions: dict | None = None
    description: str | None = None
    status: str | None = Field(default=None, max_length=50)


class PolicyRuleOut(PolicyRuleBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
