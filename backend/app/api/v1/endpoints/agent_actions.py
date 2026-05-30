from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.agent_action import (
    create_agent_action,
    delete_agent_action,
    get_agent_action,
    get_agent_actions,
    update_agent_action,
)
from app.schemas.agent_action import AgentActionCreate, AgentActionOut, AgentActionUpdate

router = APIRouter()


@router.post("/", response_model=AgentActionOut)
def create(agent_action_in: AgentActionCreate, db: Session = Depends(get_db)):
    try:
        return create_agent_action(db=db, agent_action_in=agent_action_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[AgentActionOut])
def read_all(
    tenant_id: UUID,
    status: str | None = None,
    agent_name: str | None = None,
    action_type: str | None = None,
    target_type: str | None = None,
    target_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_agent_actions(
        db=db,
        tenant_id=tenant_id,
        status=status,
        agent_name=agent_name,
        action_type=action_type,
        target_type=target_type,
        target_id=target_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{agent_action_id}", response_model=AgentActionOut)
def read(agent_action_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    agent_action = get_agent_action(
        db=db,
        agent_action_id=agent_action_id,
        tenant_id=tenant_id,
    )
    if not agent_action:
        raise HTTPException(status_code=404, detail="Agent action not found")
    return agent_action


@router.put("/{agent_action_id}", response_model=AgentActionOut)
def update(
    agent_action_id: UUID,
    tenant_id: UUID,
    agent_action_in: AgentActionUpdate,
    db: Session = Depends(get_db),
):
    agent_action = get_agent_action(
        db=db,
        agent_action_id=agent_action_id,
        tenant_id=tenant_id,
    )
    if not agent_action:
        raise HTTPException(status_code=404, detail="Agent action not found")

    try:
        return update_agent_action(
            db=db,
            agent_action=agent_action,
            agent_action_in=agent_action_in,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/{agent_action_id}", response_model=AgentActionOut)
def deactivate(agent_action_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    agent_action = delete_agent_action(
        db=db,
        agent_action_id=agent_action_id,
        tenant_id=tenant_id,
    )
    if not agent_action:
        raise HTTPException(status_code=404, detail="Agent action not found")
    return agent_action
