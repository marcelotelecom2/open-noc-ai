from uuid import UUID

from pydantic import BaseModel, Field


class CarrierBase(BaseModel):
    name: str = Field(..., max_length=255)
    type: str = Field(..., max_length=50)


class CarrierCreate(CarrierBase):
    tenant_id: UUID


class CarrierUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    type: str | None = Field(default=None, max_length=50)


class CarrierOut(CarrierBase):
    id: UUID
    tenant_id: UUID
    is_active: bool

    class Config:
        from_attributes = True
