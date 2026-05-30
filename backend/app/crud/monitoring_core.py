from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.monitoring import _validate_monitored_resource
from app.models.alert_rule import AlertRule
from app.models.check_result import CheckResult
from app.models.metric_sample import MetricSample
from app.models.monitoring_check import MonitoringCheck
from app.schemas.alert_rule import AlertRuleCreate, AlertRuleUpdate
from app.schemas.check_result import CheckResultCreate
from app.schemas.metric_sample import MetricSampleCreate
from app.schemas.monitoring_check import MonitoringCheckCreate, MonitoringCheckUpdate


def create_monitoring_check(db: Session, check_in: MonitoringCheckCreate) -> MonitoringCheck:
    _validate_monitored_resource(
        db=db,
        tenant_id=check_in.tenant_id,
        resource_type=check_in.resource_type,
        resource_id=check_in.resource_id,
    )
    check = MonitoringCheck(**check_in.model_dump(), is_active=True)
    db.add(check)
    db.commit()
    db.refresh(check)
    return check


def get_monitoring_check(db: Session, check_id: UUID, tenant_id: UUID) -> MonitoringCheck | None:
    return (
        db.query(MonitoringCheck)
        .filter(MonitoringCheck.id == check_id)
        .filter(MonitoringCheck.tenant_id == tenant_id)
        .filter(MonitoringCheck.is_active.is_(True))
        .first()
    )


def get_monitoring_checks(db: Session, tenant_id: UUID, resource_type: str | None = None, skip: int = 0, limit: int = 100):
    query = db.query(MonitoringCheck).filter(MonitoringCheck.tenant_id == tenant_id).filter(MonitoringCheck.is_active.is_(True))
    if resource_type is not None:
        query = query.filter(MonitoringCheck.resource_type == resource_type)
    return query.offset(skip).limit(limit).all()


def update_monitoring_check(db: Session, check: MonitoringCheck, check_in: MonitoringCheckUpdate) -> MonitoringCheck:
    for field, value in check_in.model_dump(exclude_unset=True).items():
        setattr(check, field, value)
    db.add(check)
    db.commit()
    db.refresh(check)
    return check


def delete_monitoring_check(db: Session, check_id: UUID, tenant_id: UUID) -> MonitoringCheck | None:
    check = get_monitoring_check(db=db, check_id=check_id, tenant_id=tenant_id)
    if not check:
        return None
    check.is_active = False
    db.add(check)
    db.commit()
    db.refresh(check)
    return check


def create_check_result(db: Session, result_in: CheckResultCreate) -> CheckResult:
    check = get_monitoring_check(db=db, check_id=result_in.monitoring_check_id, tenant_id=result_in.tenant_id)
    if not check:
        raise ValueError("Monitoring check not found")
    result = CheckResult(**result_in.model_dump(), is_active=True)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def get_check_results(db: Session, tenant_id: UUID, monitoring_check_id: UUID | None = None, skip: int = 0, limit: int = 100):
    query = db.query(CheckResult).filter(CheckResult.tenant_id == tenant_id).filter(CheckResult.is_active.is_(True))
    if monitoring_check_id is not None:
        query = query.filter(CheckResult.monitoring_check_id == monitoring_check_id)
    return query.order_by(CheckResult.checked_at.desc()).offset(skip).limit(limit).all()


def create_metric_sample(db: Session, sample_in: MetricSampleCreate) -> MetricSample:
    _validate_monitored_resource(
        db=db,
        tenant_id=sample_in.tenant_id,
        resource_type=sample_in.resource_type,
        resource_id=sample_in.resource_id,
    )
    sample = MetricSample(**sample_in.model_dump(), is_active=True)
    db.add(sample)
    db.commit()
    db.refresh(sample)
    return sample


def get_metric_samples(
    db: Session,
    tenant_id: UUID,
    resource_type: str | None = None,
    resource_id: UUID | None = None,
    metric_name: str | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(MetricSample).filter(MetricSample.tenant_id == tenant_id).filter(MetricSample.is_active.is_(True))
    if resource_type is not None:
        query = query.filter(MetricSample.resource_type == resource_type)
    if resource_id is not None:
        query = query.filter(MetricSample.resource_id == resource_id)
    if metric_name is not None:
        query = query.filter(MetricSample.metric_name == metric_name)
    return query.order_by(MetricSample.sampled_at.desc()).offset(skip).limit(limit).all()


def create_alert_rule(db: Session, rule_in: AlertRuleCreate) -> AlertRule:
    rule = AlertRule(**rule_in.model_dump(), is_active=True)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def get_alert_rule(db: Session, rule_id: UUID, tenant_id: UUID) -> AlertRule | None:
    return (
        db.query(AlertRule)
        .filter(AlertRule.id == rule_id)
        .filter(AlertRule.tenant_id == tenant_id)
        .filter(AlertRule.is_active.is_(True))
        .first()
    )


def get_alert_rules(db: Session, tenant_id: UUID, status: str | None = None, skip: int = 0, limit: int = 100):
    query = db.query(AlertRule).filter(AlertRule.tenant_id == tenant_id).filter(AlertRule.is_active.is_(True))
    if status is not None:
        query = query.filter(AlertRule.status == status)
    return query.offset(skip).limit(limit).all()


def update_alert_rule(db: Session, rule: AlertRule, rule_in: AlertRuleUpdate) -> AlertRule:
    for field, value in rule_in.model_dump(exclude_unset=True).items():
        setattr(rule, field, value)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def delete_alert_rule(db: Session, rule_id: UUID, tenant_id: UUID) -> AlertRule | None:
    rule = get_alert_rule(db=db, rule_id=rule_id, tenant_id=tenant_id)
    if not rule:
        return None
    rule.is_active = False
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule
