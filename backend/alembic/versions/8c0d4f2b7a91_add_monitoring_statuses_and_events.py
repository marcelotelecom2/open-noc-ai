"""add monitoring statuses and events

Revision ID: 8c0d4f2b7a91
Revises: 2e696eccd30d
Create Date: 2026-05-30 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8c0d4f2b7a91"
down_revision = "2e696eccd30d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "monitoring_events",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("resource_type", sa.String(length=50), nullable=False),
        sa.Column("resource_id", sa.UUID(), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("metric_name", sa.String(length=100), nullable=True),
        sa.Column("metric_value", sa.Float(), nullable=True),
        sa.Column("message", sa.String(length=500), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
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
    )
    op.create_index(
        op.f("ix_monitoring_events_event_type"),
        "monitoring_events",
        ["event_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_monitoring_events_metric_name"),
        "monitoring_events",
        ["metric_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_monitoring_events_occurred_at"),
        "monitoring_events",
        ["occurred_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_monitoring_events_resource_id"),
        "monitoring_events",
        ["resource_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_monitoring_events_resource_type"),
        "monitoring_events",
        ["resource_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_monitoring_events_severity"),
        "monitoring_events",
        ["severity"],
        unique=False,
    )
    op.create_index(
        op.f("ix_monitoring_events_status"),
        "monitoring_events",
        ["status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_monitoring_events_tenant_id"),
        "monitoring_events",
        ["tenant_id"],
        unique=False,
    )

    op.create_table(
        "monitoring_statuses",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("resource_type", sa.String(length=50), nullable=False),
        sa.Column("resource_id", sa.UUID(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("metric_name", sa.String(length=100), nullable=True),
        sa.Column("metric_value", sa.Float(), nullable=True),
        sa.Column("message", sa.String(length=500), nullable=True),
        sa.Column("last_check_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_event_at", sa.DateTime(timezone=True), nullable=True),
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
            "resource_type",
            "resource_id",
            name="uq_monitoring_status_resource",
        ),
    )
    op.create_index(
        op.f("ix_monitoring_statuses_metric_name"),
        "monitoring_statuses",
        ["metric_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_monitoring_statuses_resource_id"),
        "monitoring_statuses",
        ["resource_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_monitoring_statuses_resource_type"),
        "monitoring_statuses",
        ["resource_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_monitoring_statuses_severity"),
        "monitoring_statuses",
        ["severity"],
        unique=False,
    )
    op.create_index(
        op.f("ix_monitoring_statuses_status"),
        "monitoring_statuses",
        ["status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_monitoring_statuses_tenant_id"),
        "monitoring_statuses",
        ["tenant_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_monitoring_statuses_tenant_id"), table_name="monitoring_statuses")
    op.drop_index(op.f("ix_monitoring_statuses_status"), table_name="monitoring_statuses")
    op.drop_index(op.f("ix_monitoring_statuses_severity"), table_name="monitoring_statuses")
    op.drop_index(
        op.f("ix_monitoring_statuses_resource_type"),
        table_name="monitoring_statuses",
    )
    op.drop_index(
        op.f("ix_monitoring_statuses_resource_id"),
        table_name="monitoring_statuses",
    )
    op.drop_index(
        op.f("ix_monitoring_statuses_metric_name"),
        table_name="monitoring_statuses",
    )
    op.drop_table("monitoring_statuses")

    op.drop_index(op.f("ix_monitoring_events_tenant_id"), table_name="monitoring_events")
    op.drop_index(op.f("ix_monitoring_events_status"), table_name="monitoring_events")
    op.drop_index(op.f("ix_monitoring_events_severity"), table_name="monitoring_events")
    op.drop_index(
        op.f("ix_monitoring_events_resource_type"),
        table_name="monitoring_events",
    )
    op.drop_index(op.f("ix_monitoring_events_resource_id"), table_name="monitoring_events")
    op.drop_index(op.f("ix_monitoring_events_occurred_at"), table_name="monitoring_events")
    op.drop_index(op.f("ix_monitoring_events_metric_name"), table_name="monitoring_events")
    op.drop_index(op.f("ix_monitoring_events_event_type"), table_name="monitoring_events")
    op.drop_table("monitoring_events")
