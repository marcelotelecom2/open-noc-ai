from agents.context_selector import ContextSelector
from agents.tech_lead_gate import TechLeadGate
from tools.prompt_writer import PromptWriter


class DevelopmentGraph:
    def __init__(self):
        self.selector = ContextSelector("agent-dev-system/config/project_context.json")
        self.writer = PromptWriter()
        self.gate = TechLeadGate()

    def run(self, task: str) -> None:
        context = self.selector.select(task)

        print("\n=== CONTEXTO GERADO ===")
        print(context)

        if not self.gate.approve("Validar contexto antes de gerar prompt?"):
            print("Processo cancelado pelo Tech Lead.")
            return

        prompt = self.writer.build(context)

        print("\n=== PROMPT GERADO ===")
        print(prompt)

        if not self.gate.approve("Validar prompt antes de salvar?"):
            print("Processo cancelado pelo Tech Lead.")
            return

        with open("agent-dev-system/outputs/codex_prompt.md", "w") as f:
            f.write(prompt)

        print("\nPrompt salvo em agent-dev-system/outputs/codex_prompt.md")