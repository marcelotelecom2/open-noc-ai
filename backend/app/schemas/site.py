from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SiteBase(BaseModel):
    name: str = Field(..., max_length=255)
    city: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=50)
    is_active: bool = True


class SiteCreate(SiteBase):
    tenant_id: UUID
    customer_id: UUID


class SiteUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=50)
    is_active: bool | None = None


class SiteOut(SiteBase):
    id: UUID
    tenant_id: UUID
    customer_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
