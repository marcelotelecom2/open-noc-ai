
# 📥 INSTRUÇÃO OBRIGATÓRIA

Leia e siga RIGOROSAMENTE:

- AGENTS.md
- .ai/README.md
- .ai/rules/*
- .ai/commands/create-crud.md

---

## 🎯 TAREFA

Criar CRUD para MonitoringStatus

---

## 📌 CONTEXTO

Módulo: Monitoring
Entidade: MonitoringStatus

---

## 📚 BASE DE REFERÊNCIA

Use como base:

- backend/app/models/site.py
- backend/app/schemas/site.py
- backend/app/crud/site.py
- backend/app/api/v1/endpoints/sites.py

---

## ✏️ ESCOPO PERMITIDO

- Criar funções CRUD para MonitoringStatus
- Seguir o padrão das entidades completas do Inventory
- Aplicar filtro por tenant_id
- Respeitar soft delete com is_active

---

## 🚫 ESCOPO PROIBIDO

- Não alterar models
- Não alterar schemas
- Não alterar endpoints
- Não alterar router
- Não criar migration
- Não alterar outros módulos

---

## 📁 ARQUIVOS PERMITIDOS

- backend/app/crud/monitoring.py

---

## ⛔ ARQUIVOS PROIBIDOS

- backend/app/models/monitoring.py
- backend/app/schemas/monitoring.py
- backend/app/api/v1/endpoints/monitoring.py
- backend/app/api/router.py

---

## ✅ CRITÉRIOS DE ACEITE

- CRUD implementado
- Multi-tenant aplicado
- tenant_id obrigatório
- is_active respeitado
- padrão seguido conforme .ai
- sem acesso direto ao DB nos endpoints

---

## 🚨 REGRAS

- Não alterar arquivos fora do escopo
- Seguir padrão existente
- Não inventar arquitetura
- Parar após finalizar

