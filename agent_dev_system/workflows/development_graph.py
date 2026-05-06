import json
from pathlib import Path

from agents.architecture_guard import ArchitectureGuard
from agents.context_selector import ContextSelector
from agents.tech_lead_gate import TechLeadGate
from tools.prompt_writer import PromptWriter


TASK_PATH = Path("agent_dev_system/tasks/current_task.json")


class DevelopmentGraph:
    def __init__(self):
        self.selector = ContextSelector("agent_dev_system/config/project_context.json")
        self.guard = ArchitectureGuard()
        self.writer = PromptWriter()
        self.gate = TechLeadGate()

    def run(self, task: str) -> None:
        task_data = self._load_task()
        context = self.selector.select(task_data)

        print("\n=== CONTEXTO GERADO ===")
        print(context)

        is_valid, issues = self.guard.validate(context=context, task=task_data)

        if not is_valid:
            print("\n=== ARCHITECTURE GUARD FAILED ===")
            for issue in issues:
                print(f"- {issue}")
            return

        print("\n=== ARCHITECTURE GUARD PASSED ===")

        if not self.gate.approve("Validar contexto antes de gerar prompt?"):
            print("Processo cancelado pelo Tech Lead.")
            return

        prompt = self.writer.build(context)

        print("\n=== PROMPT GERADO ===")
        print(prompt)

        if not self.gate.approve("Validar prompt antes de salvar?"):
            print("Processo cancelado pelo Tech Lead.")
            return

        with open("agent_dev_system/outputs/codex_prompt.md", "w") as f:
            f.write(prompt)

        print("\nPrompt salvo em agent_dev_system/outputs/codex_prompt.md")

    def _load_task(self) -> dict:
        with open(TASK_PATH, "r") as f:
            return json.load(f)