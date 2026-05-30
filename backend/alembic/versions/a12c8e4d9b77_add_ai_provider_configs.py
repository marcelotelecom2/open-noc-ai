"""add ai provider configs

Revision ID: a12c8e4d9b77
Revises: f3a9b7c1d204
Create Date: 2026-05-30 00:00:02.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a12c8e4d9b77"
down_revision = "f3a9b7c1d204"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ai_provider_configs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("api_mode", sa.String(length=50), nullable=False),
        sa.Column("base_url", sa.String(length=255), nullable=False),
        sa.Column("default_model", sa.String(length=100), nullable=False),
        sa.Column("api_key_secret_name", sa.String(length=255), nullable=False),
        sa.Column("organization_id", sa.String(length=100), nullable=True),
        sa.Column("project_id", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tenant_id",
            "provider",
            name="uq_ai_provider_config_tenant_provider",
        ),
    )
    op.create_index(
        op.f("ix_ai_provider_configs_provider"),
        "ai_provider_configs",
        ["provider"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ai_provider_configs_status"),
        "ai_provider_configs",
        ["status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ai_provider_configs_tenant_id"),
        "ai_provider_configs",
        ["tenant_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_ai_provider_configs_tenant_id"), table_name="ai_provider_configs")
    op.drop_index(op.f("ix_ai_provider_configs_status"), table_name="ai_provider_configs")
    op.drop_index(op.f("ix_ai_provider_configs_provider"), table_name="ai_provider_configs")
    op.drop_table("ai_provider_configs")
