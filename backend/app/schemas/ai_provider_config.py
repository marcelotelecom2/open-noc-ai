from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AIProviderConfigBase(BaseModel):
    provider: str = Field(default="openai", max_length=50)
    api_mode: str = Field(default="responses", max_length=50)
    base_url: str = Field(default="https://api.openai.com/v1", max_length=255)
    default_model: str = Field(default="gpt-5.2", max_length=100)
    api_key_secret_name: str = Field(..., max_length=255)
    organization_id: str | None = Field(default=None, max_length=100)
    project_id: str | None = Field(default=None, max_length=100)
    status: str = Field(default="active", max_length=50)


class AIProviderConfigCreate(AIProviderConfigBase):
    tenant_id: UUID


class AIProviderConfigUpdate(BaseModel):
    api_mode: str | None = Field(default=None, max_length=50)
    base_url: str | None = Field(default=None, max_length=255)
    default_model: str | None = Field(default=None, max_length=100)
    api_key_secret_name: str | None = Field(default=None, max_length=255)
    organization_id: str | None = Field(default=None, max_length=100)
    project_id: str | None = Field(default=None, max_length=100)
    status: str | None = Field(default=None, max_length=50)


class AIProviderConfigOut(AIProviderConfigBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
