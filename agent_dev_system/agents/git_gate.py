from pathlib import Path


FINAL_REPORT = Path(
    "agent_dev_system/outputs/final_report.md"
)

OUTPUT_REPORT = Path(
    "agent_dev_system/outputs/git_gate_report.md"
)


class GitGate:
    def __init__(self):
        self.final_status = "REJECTED"
        self.reason = ""

    def execute(self):
        self._evaluate_final_report()
        self._generate_report()

        return {
            "status": self.final_status,
            "reason": self.reason,
            "report_path": str(OUTPUT_REPORT),
        }

    def _evaluate_final_report(self):
        if not FINAL_REPORT.exists():
            self.final_status = "REJECTED"
            self.reason = "Final report file not found"
            return

        content = FINAL_REPORT.read_text(
            encoding="utf-8",
        ).upper()

        if "APPROVED FOR COMMIT" in content:
            self.final_status = "APPROVED"
            self.reason = "Final report approved for commit"
            return

        if "REJECTED" in content:
            self.final_status = "REJECTED"
            self.reason = "Final report rejected"
            return

        self.final_status = "REVIEW_REQUIRED"
        self.reason = "Final report status could not be determined"

    def _generate_report(self):
        report_content = f"""# Git Gate Report

STATUS: {self.final_status}

---

## Source

agent_dev_system/outputs/final_report.md

## Decision

{self.reason}
"""

        OUTPUT_REPORT.write_text(
            report_content,
            encoding="utf-8",
        )


if __name__ == "__main__":
    result = GitGate().execute()

    print("\n=== GIT GATE RESULT ===")
    print(result)