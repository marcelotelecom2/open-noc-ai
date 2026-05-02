from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Device(Base):
    """Representa um equipamento de rede dentro de um site e tenant."""

    __tablename__ = "devices"

    # Identificação
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

    # Relacionamento
    site_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("sites.id"),
        nullable=False,
        index=True,
    )

    # Dados do dispositivo
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    ip_address: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    vendor: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Controle
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )