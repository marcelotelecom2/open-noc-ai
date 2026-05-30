from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.monitoring_core import create_metric_sample, get_metric_samples
from app.schemas.metric_sample import MetricSampleCreate, MetricSampleOut

router = APIRouter()


@router.post("/", response_model=MetricSampleOut)
def create(sample_in: MetricSampleCreate, db: Session = Depends(get_db)):
    try:
        return create_metric_sample(db=db, sample_in=sample_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[MetricSampleOut])
def read_all(
    tenant_id: UUID,
    resource_type: str | None = None,
    resource_id: UUID | None = None,
    metric_name: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_metric_samples(
        db=db,
        tenant_id=tenant_id,
        resource_type=resource_type,
        resource_id=resource_id,
        metric_name=metric_name,
        skip=skip,
        limit=limit,
    )
