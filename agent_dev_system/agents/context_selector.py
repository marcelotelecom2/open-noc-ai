from pathlib import Path
import json


class ContextSelector:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)

    def _load_config(self, path: str) -> dict:
        with open(path, "r") as f:
            return json.load(f)

    def select(self, task_input: str) -> dict:
        task_type = self._identify_task_type(task_input)
        entity = self._infer_entity_name(task_input)

        return {
            "task_type": task_type,
            "entity": entity,
            "instruction_files": self._get_instruction_files(task_type),
            "allowed_files": self._get_allowed_files(entity),
            "forbidden_files": self._get_forbidden_files(),
            "reference_files": self._get_reference_files(),
        }

    def _identify_task_type(self, task_input: str) -> str:
        task_input = task_input.lower()

        if "crud" in task_input:
            return "create_crud"
        if "model" in task_input:
            return "create_model"
        if "schema" in task_input:
            return "create_schema"
        if "endpoint" in task_input:
            return "create_endpoint"
        if "review" in task_input:
            return "review_code"

        return "unknown"

    def _get_instruction_files(self, task_type: str) -> list:
        files = []
        files.extend(self.config["instruction_files"]["always_required"])
        files.extend(self.config["instruction_files"]["backend_required"])

        command = self.config["task_commands"].get(task_type)
        if command:
            files.append(command)

        return files

    def _infer_entity_name(self, task_input: str) -> str:
        words = task_input.split()

        for word in words:
            if word[:1].isupper() and word.lower() not in ["criar", "crud", "model", "schema", "endpoint", "review"]:
                return word

        return "Unknown"

    def _get_reference_files(self) -> list:
        return [
            "backend/app/models/site.py",
            "backend/app/schemas/site.py",
            "backend/app/crud/site.py",
            "backend/app/api/v1/endpoints/sites.py",
        ]

    def _get_allowed_files(self, entity: str) -> list:
        name = self._infer_module_name(entity)

        return [
            f"backend/app/models/{name}.py",
            f"backend/app/schemas/{name}.py",
            f"backend/app/crud/{name}.py",
            f"backend/app/api/v1/endpoints/{name}.py",
        ]

    def _get_forbidden_files(self) -> list:
        return [
            "backend/app/main.py",
            "backend/app/core/",
            "backend/app/db/",
            "backend/alembic/",
            "backend/alembic.ini",
        ]

    def _infer_module_name(self, entity: str) -> str:
        if entity.lower().endswith("status"):
            return entity[:-6].lower()

        return entity.lower()