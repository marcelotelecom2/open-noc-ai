from pathlib import Path


class ReportWriter:
    def __init__(self):
        self.output_path = Path(
            "agent_dev_system/outputs/final_report.md"
        )

    def execute(
        self,
        task_data: dict,
        architecture_result: dict,
        post_codex_result: dict,
        local_validation_result: dict,
    ) -> dict:
        architecture_status = (
            "PASSED"
            if architecture_result.get(
                "approved",
                False,
            )
            else "FAILED"
        )

        post_codex_status = (
            "PASSED"
            if post_codex_result.get(
                "passed",
                False,
            )
            else "FAILED"
        )

        local_validation_status = (
            "PASSED"
            if local_validation_result.get(
                "passed",
                False,
            )
            else "FAILED"
        )

        issues = []

        issues.extend(
            architecture_result.get(
                "issues",
                [],
            )
        )

        issues.extend(
            post_codex_result.get(
                "issues",
                [],
            )
        )

        issues.extend(
            local_validation_result.get(
                "issues",
                [],
            )
        )

        final_status = (
            "APPROVED FOR COMMIT"
            if (
                architecture_status == "PASSED"
                and post_codex_status == "PASSED"
                and local_validation_status == "PASSED"
            )
            else "REJECTED"
        )

        report_content = f"""# Final Report

## Task
{task_data.get("title", "Unknown")}

## Entity
{task_data.get("entity", "Unknown")}

## Task Type
{task_data.get("type", "Unknown")}

---

# Validation Results

## Architecture Guard
{architecture_status}

## Post-Codex Validator
{post_codex_status}

## Local Validation Checklist
{local_validation_status}

---

# Issues

{self._format_issues(issues)}

---

# Final Status

{final_status}
"""

        self.output_path.write_text(
            report_content,
            encoding="utf-8",
        )

        return {
            "passed": (
                final_status
                == "APPROVED FOR COMMIT"
            ),
            "final_status": final_status,
            "issues": issues,
            "report_path": str(self.output_path),
        }

    def _format_issues(
        self,
        issues: list,
    ) -> str:
        if not issues:
            return "None"

        return "\n".join(
            [
                f"- {issue}"
                for issue in issues
            ]
        )