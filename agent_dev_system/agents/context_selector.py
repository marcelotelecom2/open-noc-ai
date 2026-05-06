import json


class ContextSelector:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)

    def _load_config(self, path: str) -> dict:
        with open(path, "r") as f:
            return json.load(f)

    def select(self, task: dict) -> dict:
        task_type = task["ai_command"].replace(".ai/commands/", "").replace(".md", "")

        return {
            "task_type": task_type,
            "entity": task["entity"],
            "instruction_files": self._get_instruction_files(task),
            "allowed_files": task["allowed_files"],
            "forbidden_files": task["forbidden_files"],
            "reference_files": self._get_reference_files(),
            "scope_allowed": task["scope_allowed"],
            "scope_forbidden": task["scope_forbidden"],
            "acceptance_criteria": task["acceptance_criteria"],
        }

    def _get_instruction_files(self, task: dict) -> list:
        files = []
        files.extend(self.config["instruction_files"]["always_required"])
        files.extend(self.config["instruction_files"]["backend_required"])
        files.append(task["ai_command"])
        return files

    def _get_reference_files(self) -> list:
        return [
            "backend/app/models/site.py",
            "backend/app/schemas/site.py",
            "backend/app/crud/site.py",
            "backend/app/api/v1/endpoints/sites.py",
        ]