from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class IncidentBase(BaseModel):
    resource_type: str = Field(..., max_length=50)
    resource_id: UUID
    title: str = Field(..., max_length=255)
    description: str | None = None
    status: str = Field(default="open", max_length=50)
    severity: str = Field(..., max_length=50)
    priority: str = Field(default="p3", max_length=50)
    monitoring_event_id: UUID | None = None
    assigned_user_id: UUID | None = None
    acknowledged_at: datetime | None = None
    resolved_at: datetime | None = None
    closed_at: datetime | None = None


class IncidentCreate(IncidentBase):
    tenant_id: UUID


class IncidentUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None
    status: str | None = Field(default=None, max_length=50)
    severity: str | None = Field(default=None, max_length=50)
    priority: str | None = Field(default=None, max_length=50)
    assigned_user_id: UUID | None = None
    acknowledged_at: datetime | None = None
    resolved_at: datetime | None = None
    closed_at: datetime | None = None
    history_message: str | None = None


class IncidentOut(IncidentBase):
    id: UUID
    tenant_id: UUID
    opened_at: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IncidentHistoryOut(BaseModel):
    id: UUID
    tenant_id: UUID
    incident_id: UUID
    action: str
    from_status: str | None
    to_status: str | None
    message: str | None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
