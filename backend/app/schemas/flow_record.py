from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class FlowRecordBase(BaseModel):
    device_id: UUID | None = None
    interface_id: UUID | None = None
    link_id: UUID | None = None
    exporter_ip: str = Field(..., max_length=50)
    flow_protocol: str = Field(..., max_length=50)
    source_ip: str = Field(..., max_length=50)
    destination_ip: str = Field(..., max_length=50)
    source_port: int | None = None
    destination_port: int | None = None
    ip_protocol: str | None = Field(default=None, max_length=20)
    direction: str | None = Field(default=None, max_length=20)
    bytes: int = 0
    packets: int = 0
    started_at: datetime | None = None
    ended_at: datetime | None = None
    raw_data: dict | None = None


class FlowRecordCreate(FlowRecordBase):
    tenant_id: UUID


class FlowRecordOut(FlowRecordBase):
    id: UUID
    tenant_id: UUID
    received_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
