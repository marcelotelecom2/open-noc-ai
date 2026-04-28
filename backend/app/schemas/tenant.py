from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TenantBase(BaseModel):
    name: str
    slug: str
    status: str
    plan: str
    is_active: bool


class TenantCreate(TenantBase):
    pass


class TenantResponse(TenantBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
