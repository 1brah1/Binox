from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class GuardrailResult:
    allowed: bool
    reason: str | None = None


class Guardrails:
    blocked_patterns = (
        "guaranteed profit",
        "insider info",
        "pump and dump",
        "100% win",
        "financial advice",
    )

    def validate_post(self, content: str) -> GuardrailResult:
        lowered = content.lower()
        for pattern in self.blocked_patterns:
            if pattern in lowered:
                return GuardrailResult(False, f"blocked phrase: {pattern}")
        if len(content.strip()) < 20:
            return GuardrailResult(False, "post too short")
        return GuardrailResult(True)

    def validate_reply(self, content: str) -> GuardrailResult:
        lowered = content.lower()
        if any(pattern in lowered for pattern in self.blocked_patterns):
            return GuardrailResult(False, "reply violates guardrails")
        if len(content.strip()) < 10:
            return GuardrailResult(False, "reply too short")
        return GuardrailResult(True)
