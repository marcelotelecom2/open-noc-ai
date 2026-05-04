from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SiteBase(BaseModel):
    name: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)


class SiteCreate(SiteBase):
    tenant_id: UUID
    customer_id: UUID


class SiteUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)


class SiteOut(SiteBase):
    id: UUID
    tenant_id: UUID
    customer_id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
