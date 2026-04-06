from __future__ import annotations

from dataclasses import dataclass

from .guardrails import Guardrails
from .models import Engagement, EngagementType


@dataclass(slots=True)
class ReplyPlan:
    kind: EngagementType
    response: str


class ReplyEngine:
    def __init__(self, guardrails: Guardrails | None = None) -> None:
        self.guardrails = guardrails or Guardrails()

    def classify(self, text: str) -> EngagementType:
        lowered = text.lower()
        if any(word in lowered for word in ("wrong", "bad", "risky", "not sure", "disagree", "weak")):
            return EngagementType.CRITIQUE
        if "?" in text or lowered.startswith(("how", "what", "why", "when", "where", "can you")):
            return EngagementType.QUESTION
        if any(word in lowered for word in ("nice", "great", "love", "good call", "solid")):
            return EngagementType.COMPLIMENT
        return EngagementType.OTHER

    def generate_reply(self, engagement: Engagement, post_text: str) -> ReplyPlan:
        kind = self.classify(engagement.text)
        if kind == EngagementType.QUESTION:
            response = (
                f"Good question. I'm watching {self._extract_focus(post_text)} for confirmation,"
                " but I'd treat this as a scenario, not a guarantee."
            )
        elif kind == EngagementType.COMPLIMENT:
            response = (
                "Appreciate it. I'm keeping the thesis simple: track the setup, wait for confirmation,"
                " and avoid forcing entries."
            )
        elif kind == EngagementType.CRITIQUE:
            response = (
                "Fair pushback. The point here is to surface a watchlist idea, not claim certainty."
                " I'd rather keep the risk framing explicit."
            )
        else:
            response = (
                "Thanks for the note. I'm keeping this high-level and focused on the setup, not on certainty."
            )

        result = self.guardrails.validate_reply(response)
        if not result.allowed:
            raise ValueError(result.reason or "reply rejected")
        return ReplyPlan(kind=kind, response=response)

    def _extract_focus(self, post_text: str) -> str:
        if ":" in post_text:
            _, focus_text = post_text.split(":", 1)
            focus_words = focus_text.strip().split()
            if focus_words:
                return " ".join(focus_words[:2])
        words = post_text.split()
        if len(words) >= 3:
            return " ".join(words[:2])
        return "the setup"
