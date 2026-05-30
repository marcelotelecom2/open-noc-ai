from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MonitoringStatusBase(BaseModel):
    resource_type: str = Field(..., max_length=50)
    resource_id: UUID
    status: str = Field(..., max_length=50)
    severity: str = Field(default="info", max_length=50)
    metric_name: str | None = Field(default=None, max_length=100)
    metric_value: float | None = None
    message: str | None = Field(default=None, max_length=500)
    last_check_at: datetime
    last_event_at: datetime | None = None


class MonitoringStatusCreate(MonitoringStatusBase):
    tenant_id: UUID


class MonitoringStatusUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=50)
    severity: str | None = Field(default=None, max_length=50)
    metric_name: str | None = Field(default=None, max_length=100)
    metric_value: float | None = None
    message: str | None = Field(default=None, max_length=500)
    last_check_at: datetime | None = None
    last_event_at: datetime | None = None


class MonitoringStatusOut(MonitoringStatusBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
