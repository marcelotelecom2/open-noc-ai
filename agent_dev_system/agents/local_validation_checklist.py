import json
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TASK_PATH = PROJECT_ROOT / "agent_dev_system/tasks/current_task.json"
CONFIG_PATH = PROJECT_ROOT / "agent_dev_system/config/project_context.json"
OUTPUT_PATH = PROJECT_ROOT / "agent_dev_system/outputs/local_validation_report.md"
GENERATED_OUTPUT_FILES = {
    "agent_dev_system/outputs/codex_prompt.md",
    "agent_dev_system/outputs/local_validation_report.md",
    "agent_dev_system/outputs/post_codex_report.md",
}


class LocalValidationChecklist:
    def run(self) -> dict:
        task = self.load_task()
        config = self.load_config()
        changed_files = self.get_changed_files()

        errors = []
        risks = []
        validations = []

        errors.extend(
            self.validate_allowed_files(
                task=task,
                changed_files=changed_files,
                validations=validations,
            )
        )
        errors.extend(
            self.validate_forbidden_files(
                task=task,
                changed_files=changed_files,
                validations=validations,
            )
        )
        errors.extend(
            self.validate_essential_files(
                task=task,
                config=config,
                validations=validations,
            )
        )
        risks.extend(
            self.collect_risks(
                task=task,
                changed_files=changed_files,
                validations=validations,
            )
        )

        status = self.resolve_status(errors=errors, risks=risks)
        result = {
            "status": status,
            "validations_executed": validations,
            "errors": errors,
            "risks": risks,
            "recommendation": self.build_recommendation(status),
        }

        self.save_report(self.build_report(result))

        print("LOCAL VALIDATION CHECKLIST:", result["status"])
        print(f"Report saved to: {OUTPUT_PATH}")

        return result

    def load_task(self) -> dict:
        with open(TASK_PATH, "r") as f:
            return json.load(f)

    def load_config(self) -> dict:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)

    def get_changed_files(self) -> list[str]:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

        changed_files = []

        for line in result.stdout.splitlines():
            if line.strip():
                changed_files.append(self.normalize_git_status_path(line))

        return changed_files

    def get_scope_changed_files(self, changed_files: list[str]) -> list[str]:
        return [
            file_path
            for file_path in changed_files
            if file_path not in GENERATED_OUTPUT_FILES
        ]

    def validate_allowed_files(
        self,
        task: dict,
        changed_files: list[str],
        validations: list[str],
    ) -> list[str]:
        validations.append("Validate changed files against allowed_files.")

        allowed_files = set(self.normalize_paths(task.get("allowed_files", [])))
        scope_changed_files = self.get_scope_changed_files(changed_files)
        issues = []

        for file_path in scope_changed_files:
            if file_path not in allowed_files:
                issues.append(f"Changed file is not allowed: {file_path}")

        return issues

    def validate_forbidden_files(
        self,
        task: dict,
        changed_files: list[str],
        validations: list[str],
    ) -> list[str]:
        validations.append("Validate changed files against forbidden_files.")

        allowed_files = set(self.normalize_paths(task.get("allowed_files", [])))
        forbidden_files = set(self.normalize_paths(task.get("forbidden_files", [])))
        scope_changed_files = self.get_scope_changed_files(changed_files)
        issues = []

        for file_path in sorted(allowed_files.intersection(forbidden_files)):
            issues.append(f"File is both allowed and forbidden: {file_path}")

        for file_path in scope_changed_files:
            if file_path in forbidden_files:
                issues.append(f"Forbidden file was changed: {file_path}")

        return issues

    def validate_essential_files(
        self,
        task: dict,
        config: dict,
        validations: list[str],
    ) -> list[str]:
        validations.append("Validate existence of essential files.")

        essential_files = []
        instruction_files = config.get("instruction_files", {})

        essential_files.extend(instruction_files.get("always_required", []))
        essential_files.extend(instruction_files.get("backend_required", []))

        ai_command = task.get("ai_command")
        if ai_command:
            essential_files.append(ai_command)

        essential_files.extend(task.get("allowed_files", []))

        issues = []

        for file_path in self.normalize_paths(essential_files):
            path = PROJECT_ROOT / file_path

            if not path.exists():
                issues.append(f"Essential file does not exist: {file_path}")

        return issues

    def collect_risks(
        self,
        task: dict,
        changed_files: list[str],
        validations: list[str],
    ) -> list[str]:
        validations.append("Collect declared task risks.")

        risks = list(task.get("risks", []))

        if not changed_files:
            risks.append("No local changed files were detected.")

        return risks

    def resolve_status(self, errors: list[str], risks: list[str]) -> str:
        if errors:
            return "FAILED"

        if risks:
            return "NEEDS_REVIEW"

        return "PASSED"

    def build_recommendation(self, status: str) -> str:
        if status == "PASSED":
            return "Prosseguir com a revisão humana final."

        if status == "FAILED":
            return "Parar o pipeline e revisar os erros antes de prosseguir."

        return "Revisar os riscos listados antes de concluir a tarefa."

    def build_report(self, result: dict) -> str:
        return f"""# Local Validation Checklist Report

## Final Status
{result["status"]}

## Validations Executed
{self.format_list(result["validations_executed"])}

## Errors
{self.format_list(result["errors"])}

## Risks
{self.format_list(result["risks"])}

## Recommendation
{result["recommendation"]}
"""

    def save_report(self, report: str) -> None:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(OUTPUT_PATH, "w") as f:
            f.write(report)

    def normalize_paths(self, paths: list[str]) -> list[str]:
        return [self.normalize_path(path) for path in paths]

    def normalize_path(self, path: str) -> str:
        return Path(path.strip()).as_posix()

    def normalize_git_status_path(self, line: str) -> str:
        path = line[3:].strip()

        if " -> " in path:
            path = path.split(" -> ", 1)[1]

        return self.normalize_path(path)

    def format_list(self, values: list[str]) -> str:
        if not values:
            return "- Nenhum"

        return "\n".join(f"- {value}" for value in values)


if __name__ == "__main__":
    checklist = LocalValidationChecklist()
    result = checklist.run()
    raise SystemExit(0 if result["status"] != "FAILED" else 1)
