from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AutomationRunBase(BaseModel):
    agent_action_id: UUID | None = None
    change_request_id: UUID | None = None
    automation_type: str = Field(..., max_length=100)
    target_type: str = Field(..., max_length=100)
    target_id: UUID | None = None
    status: str = Field(default="pending", max_length=50)
    input_payload: dict | None = None
    result_payload: dict | None = None
    error_message: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None


class AutomationRunCreate(AutomationRunBase):
    tenant_id: UUID


class AutomationRunUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=50)
    result_payload: dict | None = None
    error_message: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None


class AutomationRunOut(AutomationRunBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
