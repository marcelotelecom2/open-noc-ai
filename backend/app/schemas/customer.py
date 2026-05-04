from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CustomerBase(BaseModel):
    name: str = Field(..., max_length=255)
    document: str | None = Field(default=None, max_length=32)


class CustomerCreate(CustomerBase):
    tenant_id: UUID


class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    document: str | None = Field(default=None, max_length=32)


class CustomerOut(CustomerBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
