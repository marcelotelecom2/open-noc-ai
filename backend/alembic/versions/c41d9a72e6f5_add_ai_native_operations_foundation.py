"""add ai native operations foundation

Revision ID: c41d9a72e6f5
Revises: a12c8e4d9b77
Create Date: 2026-05-30 00:00:03.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c41d9a72e6f5"
down_revision = "a12c8e4d9b77"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "interfaces",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("device_id", sa.UUID(), nullable=False),
        sa.Column("link_id", sa.UUID(), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("mac_address", sa.String(length=50), nullable=True),
        sa.Column("ip_address", sa.String(length=50), nullable=True),
        sa.Column("speed_mbps", sa.Integer(), nullable=True),
        sa.Column("admin_status", sa.String(length=50), nullable=False),
        sa.Column("operational_status", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"]),
        sa.ForeignKeyConstraint(["link_id"], ["links.id"]),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tenant_id",
            "device_id",
            "name",
            name="uq_interfaces_tenant_device_name",
        ),
    )
    op.create_index(op.f("ix_interfaces_admin_status"), "interfaces", ["admin_status"])
    op.create_index(op.f("ix_interfaces_device_id"), "interfaces", ["device_id"])
    op.create_index(op.f("ix_interfaces_link_id"), "interfaces", ["link_id"])
    op.create_index(op.f("ix_interfaces_name"), "interfaces", ["name"])
    op.create_index(
        op.f("ix_interfaces_operational_status"),
        "interfaces",
        ["operational_status"],
    )
    op.create_index(op.f("ix_interfaces_tenant_id"), "interfaces", ["tenant_id"])

    op.create_table(
        "audit_events",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("actor_type", sa.String(length=50), nullable=False),
        sa.Column("actor_id", sa.UUID(), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("target_type", sa.String(length=100), nullable=False),
        sa.Column("target_id", sa.UUID(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("event_metadata", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_events_action"), "audit_events", ["action"])
    op.create_index(op.f("ix_audit_events_actor_id"), "audit_events", ["actor_id"])
    op.create_index(op.f("ix_audit_events_actor_type"), "audit_events", ["actor_type"])
    op.create_index(op.f("ix_audit_events_status"), "audit_events", ["status"])
    op.create_index(op.f("ix_audit_events_target_id"), "audit_events", ["target_id"])
    op.create_index(op.f("ix_audit_events_target_type"), "audit_events", ["target_type"])
    op.create_index(op.f("ix_audit_events_tenant_id"), "audit_events", ["tenant_id"])

    op.create_table(
        "agent_actions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("agent_name", sa.String(length=100), nullable=False),
        sa.Column("action_type", sa.String(length=100), nullable=False),
        sa.Column("target_type", sa.String(length=100), nullable=False),
        sa.Column("target_id", sa.UUID(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("requested_by_user_id", sa.UUID(), nullable=True),
        sa.Column("approved_by_user_id", sa.UUID(), nullable=True),
        sa.Column("input_payload", sa.JSON(), nullable=True),
        sa.Column("result_payload", sa.JSON(), nullable=True),
        sa.Column("failure_reason", sa.Text(), nullable=True),
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
        sa.ForeignKeyConstraint(["approved_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["requested_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_agent_actions_action_type"), "agent_actions", ["action_type"])
    op.create_index(
        op.f("ix_agent_actions_agent_name"),
        "agent_actions",
        ["agent_name"],
    )
    op.create_index(
        op.f("ix_agent_actions_approved_by_user_id"),
        "agent_actions",
        ["approved_by_user_id"],
    )
    op.create_index(
        op.f("ix_agent_actions_requested_by_user_id"),
        "agent_actions",
        ["requested_by_user_id"],
    )
    op.create_index(op.f("ix_agent_actions_status"), "agent_actions", ["status"])
    op.create_index(op.f("ix_agent_actions_target_id"), "agent_actions", ["target_id"])
    op.create_index(
        op.f("ix_agent_actions_target_type"),
        "agent_actions",
        ["target_type"],
    )
    op.create_index(op.f("ix_agent_actions_tenant_id"), "agent_actions", ["tenant_id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_agent_actions_tenant_id"), table_name="agent_actions")
    op.drop_index(op.f("ix_agent_actions_target_type"), table_name="agent_actions")
    op.drop_index(op.f("ix_agent_actions_target_id"), table_name="agent_actions")
    op.drop_index(op.f("ix_agent_actions_status"), table_name="agent_actions")
    op.drop_index(
        op.f("ix_agent_actions_requested_by_user_id"),
        table_name="agent_actions",
    )
    op.drop_index(
        op.f("ix_agent_actions_approved_by_user_id"),
        table_name="agent_actions",
    )
    op.drop_index(op.f("ix_agent_actions_agent_name"), table_name="agent_actions")
    op.drop_index(op.f("ix_agent_actions_action_type"), table_name="agent_actions")
    op.drop_table("agent_actions")

    op.drop_index(op.f("ix_audit_events_tenant_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_target_type"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_target_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_status"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_actor_type"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_actor_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_action"), table_name="audit_events")
    op.drop_table("audit_events")

    op.drop_index(op.f("ix_interfaces_tenant_id"), table_name="interfaces")
    op.drop_index(op.f("ix_interfaces_operational_status"), table_name="interfaces")
    op.drop_index(op.f("ix_interfaces_name"), table_name="interfaces")
    op.drop_index(op.f("ix_interfaces_link_id"), table_name="interfaces")
    op.drop_index(op.f("ix_interfaces_device_id"), table_name="interfaces")
    op.drop_index(op.f("ix_interfaces_admin_status"), table_name="interfaces")
    op.drop_table("interfaces")
