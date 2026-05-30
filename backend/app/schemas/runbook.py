from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class RunbookBase(BaseModel):
    name: str = Field(..., max_length=255)
    trigger_type: str | None = Field(default=None, max_length=100)
    resource_type: str | None = Field(default=None, max_length=50)
    severity: str | None = Field(default=None, max_length=50)
    steps: list | None = None
    expected_evidence: list | None = None
    rollback_guidance: str | None = None
    status: str = Field(default="active", max_length=50)


class RunbookCreate(RunbookBase):
    tenant_id: UUID


class RunbookUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    steps: list | None = None
    expected_evidence: list | None = None
    rollback_guidance: str | None = None
    status: str | None = Field(default=None, max_length=50)


class RunbookOut(RunbookBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
