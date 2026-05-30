from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MonitoringCheckBase(BaseModel):
    resource_type: str = Field(..., max_length=50)
    resource_id: UUID
    check_type: str = Field(..., max_length=50)
    name: str = Field(..., max_length=255)
    interval_seconds: int = 60
    timeout_seconds: int = 10
    config: dict | None = None
    status: str = Field(default="active", max_length=50)


class MonitoringCheckCreate(MonitoringCheckBase):
    tenant_id: UUID


class MonitoringCheckUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    interval_seconds: int | None = None
    timeout_seconds: int | None = None
    config: dict | None = None
    status: str | None = Field(default=None, max_length=50)


class MonitoringCheckOut(MonitoringCheckBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
