# 🧠 Task Definition Rules — open-noc-ai

## 🎯 Objetivo

Definir o padrão obrigatório para criação de microtarefas no projeto open-noc-ai.

Essas regras garantem:

- controle de escopo
- consistência técnica
- compatibilidade com agentes
- execução segura via Codex

---

## 🔴 Regra principal

Nenhuma tarefa pode ser executada sem seguir este padrão.

---

## 🧩 Estrutura obrigatória de uma tarefa

Toda tarefa DEVE conter:

### 1. Título

Descrição clara e objetiva.

Exemplo:
Criar CRUD para MonitoringStatus

---

### 2. Tipo

Um dos:

- FEATURE
- BUG
- ARCHITECTURE
- STANDARDIZATION

---

### 3. Módulo

Exemplo:

- Inventory
- Monitoring

---

### 4. Entidade

Nome técnico da entidade.

Exemplo:
MonitoringStatus

---

### 5. Objetivo

O que deve ser alcançado.

---

### 6. Escopo permitido

Lista explícita do que PODE ser feito.

---

### 7. Escopo proibido

Lista explícita do que NÃO PODE ser feito.

---

### 8. Arquivos permitidos

Lista EXATA de arquivos que podem ser modificados.

---

### 9. Arquivos proibidos

Lista EXATA de arquivos que NÃO podem ser modificados.

---

### 10. Critérios de aceite

Checklist obrigatório:

- [ ] CRUD implementado
- [ ] Multi-tenant aplicado
- [ ] tenant_id obrigatório
- [ ] is_active respeitado
- [ ] padrão seguido conforme .ai
- [ ] sem acesso direto ao DB nos endpoints

---

### 11. Comando .ai

Arquivo de comando a ser usado.

Exemplo:
.ai/commands/create-crud.md

---

### 12. Dependências

O que precisa existir antes.

---

### 13. Riscos

Possíveis problemas técnicos.

---

### 14. Status inicial

Sempre:

PLANNED

---

## 🚫 Proibições

Uma tarefa NÃO pode:

- ser genérica
- alterar múltiplos módulos sem controle
- não definir arquivos permitidos
- não definir arquivos proibidos
- não ter critérios de aceite
- depender de interpretação livre do agente

---

## 🔒 Regra de execução

Uma tarefa só pode ser executada se:

- estiver completa
- estiver validada
- estiver aprovada pelo Tech Lead