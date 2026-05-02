from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Link(Base):
    """Representa um link de conectividade de um site dentro de um tenant."""

    __tablename__ = "links"

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

    # Relacionamentos
    site_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("sites.id"),
        nullable=False,
        index=True,
    )

    carrier_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("carriers.id"),
        nullable=False,
        index=True,
    )

    # Dados do link
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    bandwidth: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="up",
    )

    # Controle
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )