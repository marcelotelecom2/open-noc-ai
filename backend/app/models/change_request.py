from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ChangeRequest(Base):
    """Representa uma mudança operacional controlada dentro do NOC."""

    __tablename__ = "change_requests"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    incident_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("incidents.id"), nullable=True, index=True)
    agent_action_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("agent_actions.id"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True)
    requested_by_user_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    approved_by_user_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    planned_start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    planned_end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rollback_plan: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
