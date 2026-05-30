from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.ai_native_operations import create_policy_rule, delete_policy_rule, get_policy_rule, get_policy_rules, update_policy_rule
from app.schemas.policy_rule import PolicyRuleCreate, PolicyRuleOut, PolicyRuleUpdate

router = APIRouter()


@router.post("/", response_model=PolicyRuleOut)
def create(rule_in: PolicyRuleCreate, db: Session = Depends(get_db)):
    try:
        return create_policy_rule(db=db, rule_in=rule_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[PolicyRuleOut])
def read_all(tenant_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_policy_rules(db=db, tenant_id=tenant_id, skip=skip, limit=limit)


@router.get("/{rule_id}", response_model=PolicyRuleOut)
def read(rule_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    rule = get_policy_rule(db=db, rule_id=rule_id, tenant_id=tenant_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Policy rule not found")
    return rule


@router.put("/{rule_id}", response_model=PolicyRuleOut)
def update(rule_id: UUID, tenant_id: UUID, rule_in: PolicyRuleUpdate, db: Session = Depends(get_db)):
    rule = get_policy_rule(db=db, rule_id=rule_id, tenant_id=tenant_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Policy rule not found")
    return update_policy_rule(db=db, rule=rule, rule_in=rule_in)


@router.delete("/{rule_id}", response_model=PolicyRuleOut)
def deactivate(rule_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    rule = delete_policy_rule(db=db, rule_id=rule_id, tenant_id=tenant_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Policy rule not found")
    return rule
