from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MetricSampleBase(BaseModel):
    resource_type: str = Field(..., max_length=50)
    resource_id: UUID
    metric_name: str = Field(..., max_length=100)
    metric_value: float
    unit: str | None = Field(default=None, max_length=50)
    sampled_at: datetime


class MetricSampleCreate(MetricSampleBase):
    tenant_id: UUID


class MetricSampleOut(MetricSampleBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
