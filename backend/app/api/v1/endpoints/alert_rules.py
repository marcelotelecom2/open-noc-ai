from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.monitoring_core import create_alert_rule, delete_alert_rule, get_alert_rule, get_alert_rules, update_alert_rule
from app.schemas.alert_rule import AlertRuleCreate, AlertRuleOut, AlertRuleUpdate

router = APIRouter()


@router.post("/", response_model=AlertRuleOut)
def create(rule_in: AlertRuleCreate, db: Session = Depends(get_db)):
    return create_alert_rule(db=db, rule_in=rule_in)


@router.get("/", response_model=list[AlertRuleOut])
def read_all(tenant_id: UUID, status: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_alert_rules(db=db, tenant_id=tenant_id, status=status, skip=skip, limit=limit)


@router.get("/{rule_id}", response_model=AlertRuleOut)
def read(rule_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    rule = get_alert_rule(db=db, rule_id=rule_id, tenant_id=tenant_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    return rule


@router.put("/{rule_id}", response_model=AlertRuleOut)
def update(rule_id: UUID, tenant_id: UUID, rule_in: AlertRuleUpdate, db: Session = Depends(get_db)):
    rule = get_alert_rule(db=db, rule_id=rule_id, tenant_id=tenant_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    return update_alert_rule(db=db, rule=rule, rule_in=rule_in)


@router.delete("/{rule_id}", response_model=AlertRuleOut)
def deactivate(rule_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    rule = delete_alert_rule(db=db, rule_id=rule_id, tenant_id=tenant_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    return rule
