from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AlertRuleBase(BaseModel):
    name: str = Field(..., max_length=255)
    resource_type: str | None = Field(default=None, max_length=50)
    metric_name: str | None = Field(default=None, max_length=100)
    condition: str = Field(..., max_length=50)
    threshold: float | None = None
    severity: str = Field(..., max_length=50)
    priority: str = Field(default="p3", max_length=50)
    window_seconds: int | None = None
    description: str | None = None
    rule_metadata: dict | None = None
    status: str = Field(default="active", max_length=50)


class AlertRuleCreate(AlertRuleBase):
    tenant_id: UUID


class AlertRuleUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    condition: str | None = Field(default=None, max_length=50)
    threshold: float | None = None
    severity: str | None = Field(default=None, max_length=50)
    priority: str | None = Field(default=None, max_length=50)
    window_seconds: int | None = None
    description: str | None = None
    rule_metadata: dict | None = None
    status: str | None = Field(default=None, max_length=50)


class AlertRuleOut(AlertRuleBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
