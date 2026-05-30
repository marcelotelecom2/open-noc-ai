from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, JSON, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SNMPTrap(Base):
    """Representa um trap SNMP recebido de equipamento de rede."""

    __tablename__ = "snmp_traps"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    device_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("devices.id"), nullable=True, index=True)
    source_ip: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    snmp_version: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    enterprise_oid: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    trap_oid: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    uptime_ticks: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    severity: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    varbinds: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
