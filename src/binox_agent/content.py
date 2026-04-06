from __future__ import annotations

from dataclasses import dataclass
import random

from .guardrails import Guardrails


@dataclass(slots=True)
class ThemeSpec:
    name: str
    voice: str
    topics: list[str]
    call_to_action: str


class ContentGenerator:
    def __init__(self, theme: ThemeSpec, guardrails: Guardrails | None = None) -> None:
        self.theme = theme
        self.guardrails = guardrails or Guardrails()

    def generate(self, seed: int | None = None) -> str:
        rng = random.Random(seed)
        topic = rng.choice(self.theme.topics)
        templates = [
            f"{self.theme.voice}: {topic} is showing a setup worth tracking. {self.theme.call_to_action}",
            f"{self.theme.voice}: early signal for {topic}; momentum is still noisy, but the structure is improving. {self.theme.call_to_action}",
            f"{self.theme.voice}: {topic} is one of the cleaner names to monitor this week. {self.theme.call_to_action}",
        ]
        post = rng.choice(templates)
        result = self.guardrails.validate_post(post)
        if not result.allowed:
            raise ValueError(result.reason or "post rejected")
        return post
