from uuid import UUID

from pydantic import BaseModel, Field


class LinkBase(BaseModel):
    tenant_id: UUID
    site_id: UUID
    carrier_id: UUID
    type: str = Field(..., max_length=50)
    bandwidth: int
    status: str = Field(default="up", max_length=50)
    is_active: bool = True


class LinkCreate(LinkBase):
    pass


class LinkUpdate(BaseModel):
    tenant_id: UUID | None = None
    site_id: UUID | None = None
    carrier_id: UUID | None = None
    type: str | None = Field(default=None, max_length=50)
    bandwidth: int | None = None
    status: str | None = Field(default=None, max_length=50)
    is_active: bool | None = None


class LinkOut(LinkBase):
    id: UUID

    class Config:
        from_attributes = True
