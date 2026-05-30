from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AgentActionBase(BaseModel):
    agent_name: str = Field(..., max_length=100)
    action_type: str = Field(..., max_length=100)
    target_type: str = Field(..., max_length=100)
    target_id: UUID | None = None
    status: str = Field(default="proposed", max_length=50)
    requested_by_user_id: UUID | None = None
    approved_by_user_id: UUID | None = None
    input_payload: dict | None = None
    result_payload: dict | None = None
    failure_reason: str | None = None


class AgentActionCreate(AgentActionBase):
    tenant_id: UUID


class AgentActionUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=50)
    approved_by_user_id: UUID | None = None
    result_payload: dict | None = None
    failure_reason: str | None = None


class AgentActionOut(AgentActionBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
