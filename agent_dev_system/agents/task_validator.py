import json
import re
import sys
from pathlib import Path

# 🔧 Ajuste de path para permitir imports internos
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "agent_dev_system"))

from tools.backend_mapper import classify_backend


TASK_PATH = Path("agent_dev_system/tasks/current_task.json")


def to_snake_case(value: str):
    value = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    return value.lower()


def load_task():
    with open(TASK_PATH, "r") as f:
        return json.load(f)


def validate_required_fields(task: dict):
    required_fields = [
        "title",
        "type",
        "module",
        "entity",
        "objective",
        "scope_allowed",
        "scope_forbidden",
        "allowed_files",
        "forbidden_files",
        "acceptance_criteria",
        "ai_command",
    ]

    missing = [field for field in required_fields if not task.get(field)]

    if missing:
        return False, f"Missing fields: {missing}"

    return True, "OK"


def validate_entity_state(task: dict):
    entity = to_snake_case(task["entity"])

    backend = classify_backend()
    complete = backend["complete_entities"]
    incomplete = backend["incomplete_entities"]

    if entity in complete:
        return False, f"Entity '{entity}' already complete. Task should not run."

    if entity not in incomplete:
        return False, f"Entity '{entity}' not found in backend."

    return True, f"Entity '{entity}' valid for execution"


def validate_approval(task: dict):
    if not task.get("approved_for_dev"):
        return False, "Task not approved for development."

    return True, "Approved"


def run_validation():
    task = load_task()

    checks = [
        validate_required_fields,
        validate_entity_state,
        validate_approval,
    ]

    for check in checks:
        valid, message = check(task)
        if not valid:
            print(f"❌ VALIDATION FAILED: {message}")
            return False

    print("✅ TASK VALIDATION PASSED")
    return True


if __name__ == "__main__":
    run_validation()
    