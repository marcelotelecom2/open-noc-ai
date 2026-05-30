from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AuditEventBase(BaseModel):
    actor_type: str = Field(..., max_length=50)
    actor_id: UUID | None = None
    action: str = Field(..., max_length=100)
    target_type: str = Field(..., max_length=100)
    target_id: UUID | None = None
    status: str = Field(default="succeeded", max_length=50)
    message: str | None = None
    event_metadata: dict | None = None


class AuditEventCreate(AuditEventBase):
    tenant_id: UUID


class AuditEventOut(AuditEventBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
