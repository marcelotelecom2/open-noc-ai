# 🏗️ ARCHITECTURE DECISIONS — agent-dev-system

## 📌 Decisão 1 — Uso do diretório .ai como fonte de verdade

### Contexto

O projeto já possui um diretório `.ai` contendo:

- regras de arquitetura
- comandos de desenvolvimento
- papéis de agentes

### Decisão

O `.ai` será tratado como:

> fonte oficial de instruções para o Codex e para o agent-dev-system

O sistema não irá duplicar essas regras, apenas selecioná-las.

### Impacto

- evita duplicação de lógica
- mantém consistência com o Codex
- centraliza governança

---

## 📌 Decisão 2 — Context Selector como núcleo do sistema

### Contexto

O principal problema identificado foi:

> perda de contexto e prompts inconsistentes

### Decisão

Criar um agente dedicado:

> ContextSelector

Responsável por:

- selecionar arquivos de instrução
- definir escopo permitido
- definir escopo proibido
- identificar entidade e tipo de tarefa

### Impacto

- elimina dependência de memória humana
- reduz erro em prompts
- garante padronização

---

## 📌 Decisão 3 — Prompt gerado automaticamente

### Contexto

Criação manual de prompts gerava inconsistência.

### Decisão

Criar:

> PromptWriter

Responsável por gerar prompts estruturados com:

- instrução obrigatória
- base de referência
- escopo permitido
- escopo proibido

### Impacto

- padronização completa
- redução de erro humano
- maior aderência do Codex

---

## 📌 Decisão 4 — Tech Lead Gate obrigatório

### Contexto

Automação total pode gerar risco de alteração indevida.

### Decisão

Implementar:

> TechLeadGate

Com validação obrigatória:

- antes de gerar prompt
- antes de salvar prompt

### Impacto

- controle humano no fluxo
- redução de risco
- alinhamento com governança

---

## 📌 Decisão 5 — Remoção de dependência externa (YAML)

### Contexto

Erro de rede impediu uso do PyYAML.

### Decisão

Utilizar JSON como formato de configuração.

### Impacto

- zero dependência externa
- maior portabilidade
- execução offline

---

## 📌 Status

Decisões implementadas no MVP inicial