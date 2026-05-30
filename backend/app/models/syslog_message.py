from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SyslogMessage(Base):
    """Representa uma mensagem syslog recebida de equipamento de rede."""

    __tablename__ = "syslog_messages"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    device_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("devices.id"), nullable=True, index=True)
    source_ip: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    transport: Mapped[str] = mapped_column(String(20), nullable=False, default="udp")
    syslog_format: Mapped[str] = mapped_column(String(50), nullable=False, default="rfc5424", index=True)
    priority: Mapped[int | None] = mapped_column(Integer, nullable=True)
    facility: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    severity: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    event_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    hostname: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    app_name: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    procid: Mapped[str | None] = mapped_column(String(100), nullable=True)
    msgid: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    structured_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_message: Mapped[str] = mapped_column(Text, nullable=False)
    parse_status: Mapped[str] = mapped_column(String(50), nullable=False, default="parsed", index=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
