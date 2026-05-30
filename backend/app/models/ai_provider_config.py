from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AIProviderConfig(Base):
    """Representa a configuração de um provedor público de IA por tenant."""

    __tablename__ = "ai_provider_configs"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "provider",
            name="uq_ai_provider_config_tenant_provider",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    tenant_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="openai",
        index=True,
    )

    api_mode: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="responses",
    )

    base_url: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="https://api.openai.com/v1",
    )

    default_model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="gpt-5.2",
    )

    api_key_secret_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    organization_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    project_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
