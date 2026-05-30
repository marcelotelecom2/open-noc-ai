from uuid import UUID

from pydantic import BaseModel, Field


class InterfaceBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = Field(default=None, max_length=255)
    type: str = Field(default="ethernet", max_length=50)
    mac_address: str | None = Field(default=None, max_length=50)
    ip_address: str | None = Field(default=None, max_length=50)
    speed_mbps: int | None = None
    admin_status: str = Field(default="up", max_length=50)
    operational_status: str = Field(default="unknown", max_length=50)


class InterfaceCreate(InterfaceBase):
    tenant_id: UUID
    device_id: UUID
    link_id: UUID | None = None


class InterfaceUpdate(BaseModel):
    link_id: UUID | None = None
    name: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    type: str | None = Field(default=None, max_length=50)
    mac_address: str | None = Field(default=None, max_length=50)
    ip_address: str | None = Field(default=None, max_length=50)
    speed_mbps: int | None = None
    admin_status: str | None = Field(default=None, max_length=50)
    operational_status: str | None = Field(default=None, max_length=50)


class InterfaceOut(InterfaceBase):
    id: UUID
    tenant_id: UUID
    device_id: UUID
    link_id: UUID | None
    is_active: bool

    class Config:
        from_attributes = True
