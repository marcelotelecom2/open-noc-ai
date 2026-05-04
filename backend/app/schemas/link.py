from uuid import UUID

from pydantic import BaseModel, Field


class LinkBase(BaseModel):
    type: str = Field(..., max_length=50)
    bandwidth: int
    status: str = Field(default="up", max_length=50)


class LinkCreate(LinkBase):
    tenant_id: UUID
    site_id: UUID
    carrier_id: UUID


class LinkUpdate(BaseModel):
    site_id: UUID | None = None
    carrier_id: UUID | None = None
    type: str | None = Field(default=None, max_length=50)
    bandwidth: int | None = None
    status: str | None = Field(default=None, max_length=50)


class LinkOut(LinkBase):
    id: UUID
    tenant_id: UUID
    site_id: UUID
    carrier_id: UUID
    is_active: bool

    class Config:
        from_attributes = True
