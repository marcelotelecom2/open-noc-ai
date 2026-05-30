"""add incidents and history

Revision ID: f3a9b7c1d204
Revises: 8c0d4f2b7a91
Create Date: 2026-05-30 00:00:01.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f3a9b7c1d204"
down_revision = "8c0d4f2b7a91"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "incidents",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("monitoring_event_id", sa.UUID(), nullable=True),
        sa.Column("resource_type", sa.String(length=50), nullable=False),
        sa.Column("resource_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("assigned_user_id", sa.UUID(), nullable=True),
        sa.Column(
            "opened_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
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
        sa.ForeignKeyConstraint(["assigned_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["monitoring_event_id"], ["monitoring_events.id"]),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_incidents_assigned_user_id"),
        "incidents",
        ["assigned_user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_incidents_monitoring_event_id"),
        "incidents",
        ["monitoring_event_id"],
        unique=False,
    )
    op.create_index(op.f("ix_incidents_priority"), "incidents", ["priority"], unique=False)
    op.create_index(
        op.f("ix_incidents_resource_id"),
        "incidents",
        ["resource_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_incidents_resource_type"),
        "incidents",
        ["resource_type"],
        unique=False,
    )
    op.create_index(op.f("ix_incidents_severity"), "incidents", ["severity"], unique=False)
    op.create_index(op.f("ix_incidents_status"), "incidents", ["status"], unique=False)
    op.create_index(
        op.f("ix_incidents_tenant_id"),
        "incidents",
        ["tenant_id"],
        unique=False,
    )

    op.create_table(
        "incident_history",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("incident_id", sa.UUID(), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("from_status", sa.String(length=50), nullable=True),
        sa.Column("to_status", sa.String(length=50), nullable=True),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["incident_id"], ["incidents.id"]),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_incident_history_action"),
        "incident_history",
        ["action"],
        unique=False,
    )
    op.create_index(
        op.f("ix_incident_history_incident_id"),
        "incident_history",
        ["incident_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_incident_history_tenant_id"),
        "incident_history",
        ["tenant_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_incident_history_tenant_id"), table_name="incident_history")
    op.drop_index(op.f("ix_incident_history_incident_id"), table_name="incident_history")
    op.drop_index(op.f("ix_incident_history_action"), table_name="incident_history")
    op.drop_table("incident_history")

    op.drop_index(op.f("ix_incidents_tenant_id"), table_name="incidents")
    op.drop_index(op.f("ix_incidents_status"), table_name="incidents")
    op.drop_index(op.f("ix_incidents_severity"), table_name="incidents")
    op.drop_index(op.f("ix_incidents_resource_type"), table_name="incidents")
    op.drop_index(op.f("ix_incidents_resource_id"), table_name="incidents")
    op.drop_index(op.f("ix_incidents_priority"), table_name="incidents")
    op.drop_index(op.f("ix_incidents_monitoring_event_id"), table_name="incidents")
    op.drop_index(op.f("ix_incidents_assigned_user_id"), table_name="incidents")
    op.drop_table("incidents")
