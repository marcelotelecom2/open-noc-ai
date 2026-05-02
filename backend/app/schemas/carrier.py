from uuid import UUID

from pydantic import BaseModel, Field


class CarrierBase(BaseModel):
    tenant_id: UUID
    name: str = Field(..., max_length=255)
    type: str = Field(..., max_length=50)
    is_active: bool = True


class CarrierCreate(CarrierBase):
    pass


class CarrierUpdate(BaseModel):
    tenant_id: UUID | None = None
    name: str | None = Field(default=None, max_length=255)
    type: str | None = Field(default=None, max_length=50)
    is_active: bool | None = None


class CarrierOut(CarrierBase):
    id: UUID

    class Config:
        from_attributes = True
