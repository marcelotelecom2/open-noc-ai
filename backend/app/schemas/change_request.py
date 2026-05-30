from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ChangeRequestBase(BaseModel):
    incident_id: UUID | None = None
    agent_action_id: UUID | None = None
    title: str = Field(..., max_length=255)
    description: str | None = None
    risk_level: str = Field(default="medium", max_length=50)
    status: str = Field(default="draft", max_length=50)
    requested_by_user_id: UUID | None = None
    approved_by_user_id: UUID | None = None
    planned_start_at: datetime | None = None
    planned_end_at: datetime | None = None
    rollback_plan: str | None = None


class ChangeRequestCreate(ChangeRequestBase):
    tenant_id: UUID


class ChangeRequestUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None
    risk_level: str | None = Field(default=None, max_length=50)
    status: str | None = Field(default=None, max_length=50)
    approved_by_user_id: UUID | None = None
    planned_start_at: datetime | None = None
    planned_end_at: datetime | None = None
    rollback_plan: str | None = None


class ChangeRequestOut(ChangeRequestBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
