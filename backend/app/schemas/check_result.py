from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CheckResultBase(BaseModel):
    monitoring_check_id: UUID
    status: str = Field(..., max_length=50)
    latency_ms: float | None = None
    output: str | None = None
    raw_data: dict | None = None
    checked_at: datetime


class CheckResultCreate(CheckResultBase):
    tenant_id: UUID


class CheckResultOut(CheckResultBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
