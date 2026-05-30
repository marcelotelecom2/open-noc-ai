from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AIRunBase(BaseModel):
    ai_provider_config_id: UUID
    agent_action_id: UUID | None = None
    target_type: str = Field(..., max_length=100)
    target_id: UUID | None = None
    purpose: str = Field(..., max_length=100)
    model: str = Field(..., max_length=100)
    status: str = Field(default="pending", max_length=50)
    input_context: dict | None = None
    prompt: str | None = None
    output: str | None = None
    error_message: str | None = None


class AIRunCreate(AIRunBase):
    tenant_id: UUID


class AIRunUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=50)
    output: str | None = None
    error_message: str | None = None


class AIRunOut(AIRunBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
