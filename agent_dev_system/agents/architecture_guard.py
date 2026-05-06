from pathlib import Path


class ArchitectureGuard:
    def validate(self, context: dict, task: dict) -> tuple[bool, list[str]]:
        """
        Validate architecture integrity before prompt generation.

        Returns:
            (is_valid, issues)
        """
        issues = []

        issues.extend(self.validate_allowed_files(context))
        issues.extend(self.validate_forbidden_files(context))
        issues.extend(self.validate_instruction_files(context))
        issues.extend(self.validate_reference_files(context))
        issues.extend(self.validate_task_approval(task))
        issues.extend(self.validate_backend_state())

        return len(issues) == 0, issues

    def validate_allowed_files(self, context: dict) -> list[str]:
        issues = []

        allowed_files = context.get("allowed_files", [])

        for file_path in allowed_files:
            path = Path(file_path)

            if not path.parent.exists():
                issues.append(
                    f"Allowed file directory does not exist: {path.parent}"
                )

        return issues

    def validate_forbidden_files(self, context: dict) -> list[str]:
        issues = []

        allowed_files = set(context.get("allowed_files", []))
        forbidden_files = set(context.get("forbidden_files", []))

        conflicting_files = allowed_files.intersection(forbidden_files)

        for file_path in sorted(conflicting_files):
            issues.append(
                f"File cannot be both allowed and forbidden: {file_path}"
            )

        return issues

    def validate_instruction_files(self, context: dict) -> list[str]:
        issues = []

        instruction_files = context.get("instruction_files", [])

        for file_path in instruction_files:
            path = Path(file_path)

            if not path.exists():
                issues.append(
                    f"Instruction file does not exist: {file_path}"
                )

        return issues

    def validate_reference_files(self, context: dict) -> list[str]:
        issues = []

        reference_files = context.get("reference_files", [])

        for file_path in reference_files:
            path = Path(file_path)

            if not path.exists():
                issues.append(
                    f"Reference file does not exist: {file_path}"
                )

        return issues

    def validate_task_approval(self, task: dict) -> list[str]:
        issues = []

        if task.get("approved_for_dev") is not True:
            issues.append("Task is not approved for development.")

        return issues

    def validate_backend_state(self) -> list[str]:
        issues = []

        backend_path = Path("backend")

        if not backend_path.exists():
            issues.append("Backend directory does not exist.")

        return issues