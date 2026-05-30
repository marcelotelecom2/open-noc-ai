from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SNMPTrapBase(BaseModel):
    device_id: UUID | None = None
    source_ip: str = Field(..., max_length=50)
    snmp_version: str = Field(..., max_length=20)
    enterprise_oid: str | None = Field(default=None, max_length=255)
    trap_oid: str = Field(..., max_length=255)
    uptime_ticks: int | None = None
    severity: str | None = Field(default=None, max_length=50)
    varbinds: dict | None = None
    raw_data: dict | None = None


class SNMPTrapCreate(SNMPTrapBase):
    tenant_id: UUID


class SNMPTrapOut(SNMPTrapBase):
    id: UUID
    tenant_id: UUID
    received_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
