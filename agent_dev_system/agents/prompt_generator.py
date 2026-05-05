import json
import sys
from pathlib import Path

# 🔧 Ajuste de path para permitir imports internos
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "agent_dev_system"))

from tools.backend_mapper import select_reference_entity


TASK_PATH = Path("agent_dev_system/tasks/current_task.json")
OUTPUT_PATH = Path("agent_dev_system/outputs/codex_prompt.md")


def load_task():
    with open(TASK_PATH, "r") as f:
        return json.load(f)


def build_prompt(task: dict):
    reference_entity = select_reference_entity()

    prompt = f"""
# 📥 INSTRUÇÃO OBRIGATÓRIA

Leia e siga RIGOROSAMENTE:

- AGENTS.md
- .ai/README.md
- .ai/rules/*
- .ai/commands/{task["ai_command"].split("/")[-1]}

---

## 🎯 TAREFA

{task["title"]}

---

## 📌 CONTEXTO

Módulo: {task["module"]}
Entidade: {task["entity"]}

---

## 📚 BASE DE REFERÊNCIA

Use como base:

- backend/app/models/{reference_entity}.py
- backend/app/schemas/{reference_entity}.py
- backend/app/crud/{reference_entity}.py
- backend/app/api/v1/endpoints/{reference_entity}s.py

---

## ✏️ ESCOPO PERMITIDO

{chr(10).join(f"- {item}" for item in task["scope_allowed"])}

---

## 🚫 ESCOPO PROIBIDO

{chr(10).join(f"- {item}" for item in task["scope_forbidden"])}

---

## 📁 ARQUIVOS PERMITIDOS

{chr(10).join(f"- {item}" for item in task["allowed_files"])}

---

## ⛔ ARQUIVOS PROIBIDOS

{chr(10).join(f"- {item}" for item in task["forbidden_files"])}

---

## ✅ CRITÉRIOS DE ACEITE

{chr(10).join(f"- {item}" for item in task["acceptance_criteria"])}

---

## 🚨 REGRAS

- Não alterar arquivos fora do escopo
- Seguir padrão existente
- Não inventar arquitetura
- Parar após finalizar

"""

    return prompt


def save_prompt(prompt: str):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(prompt)


def run():
    task = load_task()
    prompt = build_prompt(task)
    save_prompt(prompt)

    print("✅ PROMPT GENERATED")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    run()