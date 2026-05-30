from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.tenant import get_tenant
from app.models.ai_run import AIRun
from app.models.automation_run import AutomationRun
from app.models.change_request import ChangeRequest
from app.models.policy_rule import PolicyRule
from app.models.runbook import Runbook
from app.schemas.ai_run import AIRunCreate, AIRunUpdate
from app.schemas.automation_run import AutomationRunCreate, AutomationRunUpdate
from app.schemas.change_request import ChangeRequestCreate, ChangeRequestUpdate
from app.schemas.policy_rule import PolicyRuleCreate, PolicyRuleUpdate
from app.schemas.runbook import RunbookCreate, RunbookUpdate


def _validate_tenant(db: Session, tenant_id: UUID) -> None:
    if not get_tenant(db=db, tenant_id=tenant_id):
        raise ValueError("Tenant not found")


def _get_active(db: Session, model, item_id: UUID, tenant_id: UUID):
    return (
        db.query(model)
        .filter(model.id == item_id)
        .filter(model.tenant_id == tenant_id)
        .filter(model.is_active.is_(True))
        .first()
    )


def _list_active(db: Session, model, tenant_id: UUID, skip: int, limit: int):
    return (
        db.query(model)
        .filter(model.tenant_id == tenant_id)
        .filter(model.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


def _update(db: Session, item, payload) -> object:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def _delete(db: Session, item) -> object:
    item.is_active = False
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def create_ai_run(db: Session, run_in: AIRunCreate) -> AIRun:
    _validate_tenant(db=db, tenant_id=run_in.tenant_id)
    run = AIRun(**run_in.model_dump(), is_active=True)
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def get_ai_run(db: Session, run_id: UUID, tenant_id: UUID) -> AIRun | None:
    return _get_active(db=db, model=AIRun, item_id=run_id, tenant_id=tenant_id)


def get_ai_runs(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100):
    return _list_active(db=db, model=AIRun, tenant_id=tenant_id, skip=skip, limit=limit)


def update_ai_run(db: Session, run: AIRun, run_in: AIRunUpdate) -> AIRun:
    return _update(db=db, item=run, payload=run_in)


def delete_ai_run(db: Session, run_id: UUID, tenant_id: UUID) -> AIRun | None:
    run = get_ai_run(db=db, run_id=run_id, tenant_id=tenant_id)
    return _delete(db=db, item=run) if run else None


def create_policy_rule(db: Session, rule_in: PolicyRuleCreate) -> PolicyRule:
    _validate_tenant(db=db, tenant_id=rule_in.tenant_id)
    rule = PolicyRule(**rule_in.model_dump(), is_active=True)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def get_policy_rule(db: Session, rule_id: UUID, tenant_id: UUID) -> PolicyRule | None:
    return _get_active(db=db, model=PolicyRule, item_id=rule_id, tenant_id=tenant_id)


def get_policy_rules(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100):
    return _list_active(db=db, model=PolicyRule, tenant_id=tenant_id, skip=skip, limit=limit)


def update_policy_rule(db: Session, rule: PolicyRule, rule_in: PolicyRuleUpdate) -> PolicyRule:
    return _update(db=db, item=rule, payload=rule_in)


def delete_policy_rule(db: Session, rule_id: UUID, tenant_id: UUID) -> PolicyRule | None:
    rule = get_policy_rule(db=db, rule_id=rule_id, tenant_id=tenant_id)
    return _delete(db=db, item=rule) if rule else None


def create_change_request(db: Session, change_in: ChangeRequestCreate) -> ChangeRequest:
    _validate_tenant(db=db, tenant_id=change_in.tenant_id)
    change = ChangeRequest(**change_in.model_dump(), is_active=True)
    db.add(change)
    db.commit()
    db.refresh(change)
    return change


def get_change_request(db: Session, change_id: UUID, tenant_id: UUID) -> ChangeRequest | None:
    return _get_active(db=db, model=ChangeRequest, item_id=change_id, tenant_id=tenant_id)


def get_change_requests(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100):
    return _list_active(db=db, model=ChangeRequest, tenant_id=tenant_id, skip=skip, limit=limit)


def update_change_request(db: Session, change: ChangeRequest, change_in: ChangeRequestUpdate) -> ChangeRequest:
    return _update(db=db, item=change, payload=change_in)


def delete_change_request(db: Session, change_id: UUID, tenant_id: UUID) -> ChangeRequest | None:
    change = get_change_request(db=db, change_id=change_id, tenant_id=tenant_id)
    return _delete(db=db, item=change) if change else None


def create_automation_run(db: Session, run_in: AutomationRunCreate) -> AutomationRun:
    _validate_tenant(db=db, tenant_id=run_in.tenant_id)
    run = AutomationRun(**run_in.model_dump(), is_active=True)
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def get_automation_run(db: Session, run_id: UUID, tenant_id: UUID) -> AutomationRun | None:
    return _get_active(db=db, model=AutomationRun, item_id=run_id, tenant_id=tenant_id)


def get_automation_runs(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100):
    return _list_active(db=db, model=AutomationRun, tenant_id=tenant_id, skip=skip, limit=limit)


def update_automation_run(db: Session, run: AutomationRun, run_in: AutomationRunUpdate) -> AutomationRun:
    return _update(db=db, item=run, payload=run_in)


def delete_automation_run(db: Session, run_id: UUID, tenant_id: UUID) -> AutomationRun | None:
    run = get_automation_run(db=db, run_id=run_id, tenant_id=tenant_id)
    return _delete(db=db, item=run) if run else None


def create_runbook(db: Session, runbook_in: RunbookCreate) -> Runbook:
    _validate_tenant(db=db, tenant_id=runbook_in.tenant_id)
    runbook = Runbook(**runbook_in.model_dump(), is_active=True)
    db.add(runbook)
    db.commit()
    db.refresh(runbook)
    return runbook


def get_runbook(db: Session, runbook_id: UUID, tenant_id: UUID) -> Runbook | None:
    return _get_active(db=db, model=Runbook, item_id=runbook_id, tenant_id=tenant_id)


def get_runbooks(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100):
    return _list_active(db=db, model=Runbook, tenant_id=tenant_id, skip=skip, limit=limit)


def update_runbook(db: Session, runbook: Runbook, runbook_in: RunbookUpdate) -> Runbook:
    return _update(db=db, item=runbook, payload=runbook_in)


def delete_runbook(db: Session, runbook_id: UUID, tenant_id: UUID) -> Runbook | None:
    runbook = get_runbook(db=db, runbook_id=runbook_id, tenant_id=tenant_id)
    return _delete(db=db, item=runbook) if runbook else None
