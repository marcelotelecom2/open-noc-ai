from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SyslogMessageBase(BaseModel):
    device_id: UUID | None = None
    source_ip: str = Field(..., max_length=50)
    transport: str = Field(default="udp", max_length=20)
    syslog_format: str = Field(default="rfc5424", max_length=50)
    priority: int | None = None
    facility: int | None = None
    severity: int | None = None
    version: int | None = None
    event_timestamp: datetime | None = None
    hostname: str | None = Field(default=None, max_length=255)
    app_name: str | None = Field(default=None, max_length=100)
    procid: str | None = Field(default=None, max_length=100)
    msgid: str | None = Field(default=None, max_length=100)
    structured_data: dict | None = None
    message: str | None = None
    raw_message: str
    parse_status: str = Field(default="parsed", max_length=50)


class SyslogMessageCreate(SyslogMessageBase):
    tenant_id: UUID


class SyslogMessageOut(SyslogMessageBase):
    id: UUID
    tenant_id: UUID
    received_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
