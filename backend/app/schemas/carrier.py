from uuid import UUID

from pydantic import BaseModel, Field


class CarrierBase(BaseModel):
    name: str = Field(..., max_length=255)
    type: str = Field(..., max_length=50)


class CarrierCreate(CarrierBase):
    pass


class CarrierUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    type: str | None = Field(default=None, max_length=50)


class CarrierOut(CarrierBase):
    id: UUID

    class Config:
        from_attributes = True
