from uuid import UUID

from pydantic import BaseModel, Field


class DeviceBase(BaseModel):
    name: str = Field(..., max_length=255)
    ip_address: str = Field(..., max_length=50)
    vendor: str = Field(..., max_length=100)
    model: str = Field(..., max_length=100)
    role: str = Field(..., max_length=50)
    is_active: bool = True


class DeviceCreate(DeviceBase):
    tenant_id: UUID
    site_id: UUID


class DeviceUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    ip_address: str | None = Field(default=None, max_length=50)
    vendor: str | None = Field(default=None, max_length=100)
    model: str | None = Field(default=None, max_length=100)
    role: str | None = Field(default=None, max_length=50)
    is_active: bool | None = None


class DeviceOut(DeviceBase):
    id: UUID
    tenant_id: UUID
    site_id: UUID

    class Config:
        from_attributes = True
