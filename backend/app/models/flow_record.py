from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, JSON, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class FlowRecord(Base):
    """Representa um registro de fluxo IP exportado por equipamento de rede."""

    __tablename__ = "flow_records"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    device_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("devices.id"), nullable=True, index=True)
    interface_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("interfaces.id"), nullable=True, index=True)
    link_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("links.id"), nullable=True, index=True)
    exporter_ip: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    flow_protocol: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source_ip: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    destination_ip: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source_port: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    destination_port: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    ip_protocol: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    direction: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    bytes: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    packets: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
