import json
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TASK_PATH = PROJECT_ROOT / "agent_dev_system/tasks/current_task.json"
OUTPUT_PATH = PROJECT_ROOT / "agent_dev_system/outputs/post_codex_report.md"


def normalize_path(path: str) -> str:
    return Path(path.strip()).as_posix()


def load_task() -> dict:
    with open(TASK_PATH, "r") as f:
        return json.load(f)


def get_allowed_files(task: dict) -> list[str]:
    return [normalize_path(path) for path in task.get("allowed_files", [])]


def get_changed_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    return [
        normalize_path(path)
        for path in result.stdout.splitlines()
        if path.strip()
    ]


def classify_changed_files(changed_files: list[str], allowed_files: list[str]) -> dict:
    allowed_set = set(allowed_files)
    allowed_changed = [path for path in changed_files if path in allowed_set]
    not_allowed_changed = [path for path in changed_files if path not in allowed_set]

    status = "PASSED" if not not_allowed_changed else "FAILED"

    return {
        "status": status,
        "changed_files": changed_files,
        "allowed_changed": allowed_changed,
        "not_allowed_changed": not_allowed_changed,
    }


def format_file_list(files: list[str]) -> str:
    if not files:
        return "- Nenhum"

    return "\n".join(f"- {path}" for path in files)


def build_report(classification: dict) -> str:
    status = classification["status"]

    if status == "PASSED":
        conclusion = "Todos os arquivos alterados estão dentro do escopo permitido."
        recommendation = "Prosseguir com a revisão humana da alteração."
    else:
        conclusion = "Foram encontrados arquivos alterados fora do escopo permitido."
        recommendation = "Revisar os arquivos fora do escopo antes de prosseguir."

    return f"""# Post-Codex Validator Report

## Status geral

{status}

## Arquivos alterados

{format_file_list(classification["changed_files"])}

## Arquivos permitidos alterados

{format_file_list(classification["allowed_changed"])}

## Arquivos não permitidos alterados

{format_file_list(classification["not_allowed_changed"])}

## Conclusão

{conclusion}

## Recomendação

{recommendation}
"""


def save_report(report: str) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        f.write(report)


def run() -> bool:
    task = load_task()
    allowed_files = get_allowed_files(task)
    changed_files = get_changed_files()
    classification = classify_changed_files(changed_files, allowed_files)
    report = build_report(classification)

    save_report(report)

    print("POST-CODEX VALIDATION:", classification["status"])
    print(f"Report saved to: {OUTPUT_PATH}")

    return classification["status"] == "PASSED"


if __name__ == "__main__":
    run()
