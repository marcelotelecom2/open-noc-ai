from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Runbook(Base):
    """Representa um runbook operacional consumível por humanos e agentes."""

    __tablename__ = "runbooks"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    trigger_type: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    resource_type: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    severity: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    steps: Mapped[list | None] = mapped_column(JSON, nullable=True)
    expected_evidence: Mapped[list | None] = mapped_column(JSON, nullable=True)
    rollback_guidance: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
