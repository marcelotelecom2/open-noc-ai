from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MonitoringEventBase(BaseModel):
    resource_type: str = Field(..., max_length=50)
    resource_id: UUID
    event_type: str = Field(..., max_length=50)
    status: str | None = Field(default=None, max_length=50)
    severity: str = Field(default="info", max_length=50)
    metric_name: str | None = Field(default=None, max_length=100)
    metric_value: float | None = None
    message: str | None = Field(default=None, max_length=500)
    occurred_at: datetime


class MonitoringEventCreate(MonitoringEventBase):
    tenant_id: UUID


class MonitoringEventOut(MonitoringEventBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
