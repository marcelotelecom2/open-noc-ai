class TechLeadGate:
    def approve(self, message: str) -> bool:
        print("\n=== TECH LEAD GATE ===")
        print(message)

        response = input("\nAprovar? (s/n): ").strip().lower()

        return response == "s"