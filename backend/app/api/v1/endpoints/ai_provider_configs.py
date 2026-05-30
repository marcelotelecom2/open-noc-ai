from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.ai_provider_config import (
    create_ai_provider_config,
    delete_ai_provider_config,
    get_ai_provider_config,
    get_ai_provider_configs,
    update_ai_provider_config,
)
from app.schemas.ai_provider_config import (
    AIProviderConfigCreate,
    AIProviderConfigOut,
    AIProviderConfigUpdate,
)

router = APIRouter()


@router.post("/", response_model=AIProviderConfigOut)
def create(config_in: AIProviderConfigCreate, db: Session = Depends(get_db)):
    try:
        return create_ai_provider_config(db=db, config_in=config_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[AIProviderConfigOut])
def read_all(
    tenant_id: UUID,
    provider: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_ai_provider_configs(
        db=db,
        tenant_id=tenant_id,
        provider=provider,
        skip=skip,
        limit=limit,
    )


@router.get("/{config_id}", response_model=AIProviderConfigOut)
def read(config_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    config = get_ai_provider_config(db=db, config_id=config_id, tenant_id=tenant_id)
    if not config:
        raise HTTPException(status_code=404, detail="AI provider config not found")
    return config


@router.put("/{config_id}", response_model=AIProviderConfigOut)
def update(
    config_id: UUID,
    tenant_id: UUID,
    config_in: AIProviderConfigUpdate,
    db: Session = Depends(get_db),
):
    config = get_ai_provider_config(db=db, config_id=config_id, tenant_id=tenant_id)
    if not config:
        raise HTTPException(status_code=404, detail="AI provider config not found")

    try:
        return update_ai_provider_config(db=db, config=config, config_in=config_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/{config_id}", response_model=AIProviderConfigOut)
def deactivate(config_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    config = delete_ai_provider_config(db=db, config_id=config_id, tenant_id=tenant_id)
    if not config:
        raise HTTPException(status_code=404, detail="AI provider config not found")
    return config
