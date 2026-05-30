from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.tenant import get_tenant
from app.models.ai_provider_config import AIProviderConfig
from app.schemas.ai_provider_config import (
    AIProviderConfigCreate,
    AIProviderConfigUpdate,
)

SUPPORTED_AI_PROVIDERS = {"openai"}
SUPPORTED_OPENAI_API_MODES = {"responses"}


def _validate_ai_provider(provider: str, api_mode: str) -> None:
    if provider not in SUPPORTED_AI_PROVIDERS:
        raise ValueError("Unsupported AI provider")
    if provider == "openai" and api_mode not in SUPPORTED_OPENAI_API_MODES:
        raise ValueError("Unsupported OpenAI API mode")


def create_ai_provider_config(
    db: Session,
    config_in: AIProviderConfigCreate,
) -> AIProviderConfig:
    tenant = get_tenant(db=db, tenant_id=config_in.tenant_id)
    if not tenant:
        raise ValueError("Tenant not found")

    _validate_ai_provider(provider=config_in.provider, api_mode=config_in.api_mode)

    existing_config = get_ai_provider_config_by_provider(
        db=db,
        tenant_id=config_in.tenant_id,
        provider=config_in.provider,
    )
    if existing_config:
        raise ValueError("AI provider config already exists")

    config = AIProviderConfig(
        tenant_id=config_in.tenant_id,
        provider=config_in.provider,
        api_mode=config_in.api_mode,
        base_url=config_in.base_url,
        default_model=config_in.default_model,
        api_key_secret_name=config_in.api_key_secret_name,
        organization_id=config_in.organization_id,
        project_id=config_in.project_id,
        status=config_in.status,
        is_active=True,
    )
    db.add(config)
    db.commit()
    db.refresh(config)
    return config


def get_ai_provider_config(
    db: Session,
    config_id: UUID,
    tenant_id: UUID,
) -> AIProviderConfig | None:
    return (
        db.query(AIProviderConfig)
        .filter(AIProviderConfig.id == config_id)
        .filter(AIProviderConfig.tenant_id == tenant_id)
        .filter(AIProviderConfig.is_active.is_(True))
        .first()
    )


def get_ai_provider_config_by_provider(
    db: Session,
    tenant_id: UUID,
    provider: str,
) -> AIProviderConfig | None:
    return (
        db.query(AIProviderConfig)
        .filter(AIProviderConfig.tenant_id == tenant_id)
        .filter(AIProviderConfig.provider == provider)
        .filter(AIProviderConfig.is_active.is_(True))
        .first()
    )


def get_ai_provider_configs(
    db: Session,
    tenant_id: UUID,
    provider: str | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = (
        db.query(AIProviderConfig)
        .filter(AIProviderConfig.tenant_id == tenant_id)
        .filter(AIProviderConfig.is_active.is_(True))
    )
    if provider is not None:
        query = query.filter(AIProviderConfig.provider == provider)

    return query.offset(skip).limit(limit).all()


def update_ai_provider_config(
    db: Session,
    config: AIProviderConfig,
    config_in: AIProviderConfigUpdate,
) -> AIProviderConfig:
    update_data = config_in.model_dump(exclude_unset=True)

    api_mode = update_data.get("api_mode", config.api_mode)
    _validate_ai_provider(provider=config.provider, api_mode=api_mode)

    for field, value in update_data.items():
        setattr(config, field, value)

    db.add(config)
    db.commit()
    db.refresh(config)
    return config


def delete_ai_provider_config(
    db: Session,
    config_id: UUID,
    tenant_id: UUID,
) -> AIProviderConfig | None:
    config = get_ai_provider_config(db=db, config_id=config_id, tenant_id=tenant_id)
    if not config:
        return None

    config.is_active = False
    db.add(config)
    db.commit()
    db.refresh(config)
    return config
