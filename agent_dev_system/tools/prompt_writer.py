class PromptWriter:
    def build(self, context: dict) -> str:
        lines = []

        lines.append("# 🔴 PROMPT — CODEX | open-noc-ai\n")

        # Tarefa
        lines.append("## 🎯 TAREFA\n")
        lines.append(f"Implementar {context['task_type']} para entidade {context['entity']}\n")

        # Instrução forte
        lines.append("## 📥 INSTRUÇÃO OBRIGATÓRIA\n")
        lines.append("Leia e siga RIGOROSAMENTE os arquivos abaixo ANTES de qualquer implementação:\n")

        for f in context["instruction_files"]:
            lines.append(f"- {f}")

        # Referência
        lines.append("\n## 📚 BASE DE REFERÊNCIA\n")
        lines.append("Use os arquivos abaixo como padrão de implementação:\n")

        for f in context["reference_files"]:
            lines.append(f"- {f}")

        # Escopo permitido
        lines.append("\n## ✏️ ESCOPO PERMITIDO\n")
        lines.append("Você PODE alterar APENAS os arquivos abaixo:\n")

        for f in context["allowed_files"]:
            lines.append(f"- {f}")

        # Escopo proibido
        lines.append("\n## ⛔ ESCOPO PROIBIDO\n")
        lines.append("NÃO altere NENHUM destes arquivos:\n")

        for f in context["forbidden_files"]:
            lines.append(f"- {f}")

        # Regras
        lines.append("\n## 🚨 REGRAS CRÍTICAS\n")
        lines.append("- NÃO criar arquivos fora do escopo")
        lines.append("- NÃO alterar arquivos proibidos")
        lines.append("- SEGUIR exatamente os padrões dos arquivos de referência")
        lines.append("- PARAR imediatamente após concluir a tarefa")
        lines.append("- NÃO avançar para outras tarefas")

        return "\n".join(lines)