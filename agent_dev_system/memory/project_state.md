# 📊 PROJECT STATE — agent-dev-system

## 🎯 Objetivo

Sistema multi-agente para controlar o desenvolvimento do open-noc-ai, garantindo:

- seleção correta de contexto
- geração de prompts consistentes para Codex
- controle de escopo
- validação humana (Tech Lead Gate)

---

## 🧠 Componentes implementados

### 1. Context Selector

Responsável por:

- identificar tipo da tarefa
- identificar entidade
- selecionar arquivos de instrução (.ai)
- selecionar arquivos de referência
- definir arquivos permitidos
- definir arquivos proibidos

---

### 2. Prompt Writer

Responsável por:

- gerar prompt estruturado para Codex
- reforçar leitura obrigatória dos arquivos de instrução
- definir escopo permitido e proibido
- padronizar execução da tarefa

---

### 3. Tech Lead Gate

Responsável por:

- validar contexto antes da execução
- validar prompt antes de envio ao Codex
- impedir execução automática sem aprovação

---

## 🔁 Fluxo atual (MVP)

Task Input  
→ Context Selector  
→ Tech Lead Gate  
→ Prompt Writer  
→ Tech Lead Gate  
→ outputs/codex_prompt.md  

---

## ✅ Problemas resolvidos

- ChatGPT não perde mais contexto de arquitetura
- arquivos de instrução são sempre incluídos
- escopo de alteração controlado
- redução de erro humano na criação de prompt

---

## ⚠️ Limitações atuais

- seleção de arquivos ainda é simples (baseada em regra)
- não há leitura automática do código real do projeto
- não há validação pós-Codex
- não há memória de decisões técnicas

---

## 🚀 Próximos passos

- melhorar seleção de contexto (nível avançado)
- adicionar validação automática (testes / revisão)
- implementar memória persistente (L2MAC)
- integrar com LangGraph
- criar feedback loop com Codex

---

## 📌 Status

MVP funcional concluído e validado