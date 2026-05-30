from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.tenant import get_tenant
from app.models.agent_action import AgentAction
from app.models.user import User
from app.schemas.agent_action import AgentActionCreate, AgentActionUpdate

AGENT_ACTION_STATUSES = {
    "proposed",
    "approved",
    "rejected",
    "running",
    "succeeded",
    "failed",
    "cancelled",
}


def _validate_agent_action_status(status: str) -> None:
    if status not in AGENT_ACTION_STATUSES:
        raise ValueError("Unsupported agent action status")


def _validate_user(
    db: Session,
    tenant_id: UUID,
    user_id: UUID | None,
    error_message: str,
) -> None:
    if user_id is None:
        return

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .filter(User.tenant_id == tenant_id)
        .filter(User.is_active.is_(True))
        .first()
    )
    if not user:
        raise ValueError(error_message)


def create_agent_action(
    db: Session,
    agent_action_in: AgentActionCreate,
) -> AgentAction:
    tenant = get_tenant(db=db, tenant_id=agent_action_in.tenant_id)
    if not tenant:
        raise ValueError("Tenant not found")

    _validate_agent_action_status(agent_action_in.status)
    _validate_user(
        db=db,
        tenant_id=agent_action_in.tenant_id,
        user_id=agent_action_in.requested_by_user_id,
        error_message="Requested by user not found",
    )
    _validate_user(
        db=db,
        tenant_id=agent_action_in.tenant_id,
        user_id=agent_action_in.approved_by_user_id,
        error_message="Approved by user not found",
    )

    agent_action = AgentAction(
        tenant_id=agent_action_in.tenant_id,
        agent_name=agent_action_in.agent_name,
        action_type=agent_action_in.action_type,
        target_type=agent_action_in.target_type,
        target_id=agent_action_in.target_id,
        status=agent_action_in.status,
        requested_by_user_id=agent_action_in.requested_by_user_id,
        approved_by_user_id=agent_action_in.approved_by_user_id,
        input_payload=agent_action_in.input_payload,
        result_payload=agent_action_in.result_payload,
        failure_reason=agent_action_in.failure_reason,
        is_active=True,
    )
    db.add(agent_action)
    db.commit()
    db.refresh(agent_action)
    return agent_action


def get_agent_action(
    db: Session,
    agent_action_id: UUID,
    tenant_id: UUID,
) -> AgentAction | None:
    return (
        db.query(AgentAction)
        .filter(AgentAction.id == agent_action_id)
        .filter(AgentAction.tenant_id == tenant_id)
        .filter(AgentAction.is_active.is_(True))
        .first()
    )


def get_agent_actions(
    db: Session,
    tenant_id: UUID,
    status: str | None = None,
    agent_name: str | None = None,
    action_type: str | None = None,
    target_type: str | None = None,
    target_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = (
        db.query(AgentAction)
        .filter(AgentAction.tenant_id == tenant_id)
        .filter(AgentAction.is_active.is_(True))
    )
    if status is not None:
        query = query.filter(AgentAction.status == status)
    if agent_name is not None:
        query = query.filter(AgentAction.agent_name == agent_name)
    if action_type is not None:
        query = query.filter(AgentAction.action_type == action_type)
    if target_type is not None:
        query = query.filter(AgentAction.target_type == target_type)
    if target_id is not None:
        query = query.filter(AgentAction.target_id == target_id)

    return query.order_by(AgentAction.created_at.desc()).offset(skip).limit(limit).all()


def update_agent_action(
    db: Session,
    agent_action: AgentAction,
    agent_action_in: AgentActionUpdate,
) -> AgentAction:
    update_data = agent_action_in.model_dump(exclude_unset=True)

    status = update_data.get("status", agent_action.status)
    _validate_agent_action_status(status)
    _validate_user(
        db=db,
        tenant_id=agent_action.tenant_id,
        user_id=update_data.get("approved_by_user_id", agent_action.approved_by_user_id),
        error_message="Approved by user not found",
    )

    for field, value in update_data.items():
        setattr(agent_action, field, value)

    db.add(agent_action)
    db.commit()
    db.refresh(agent_action)
    return agent_action


def delete_agent_action(
    db: Session,
    agent_action_id: UUID,
    tenant_id: UUID,
) -> AgentAction | None:
    agent_action = get_agent_action(
        db=db,
        agent_action_id=agent_action_id,
        tenant_id=tenant_id,
    )
    if not agent_action:
        return None

    agent_action.is_active = False
    db.add(agent_action)
    db.commit()
    db.refresh(agent_action)
    return agent_action
