from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class EngagementType(str, Enum):
    QUESTION = "question"
    COMPLIMENT = "compliment"
    CRITIQUE = "critique"
    OTHER = "other"


@dataclass(slots=True)
class Post:
    id: str
    theme: str
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class Engagement:
    id: str
    post_id: str
    author: str
    text: str
    kind: EngagementType
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class Reply:
    engagement_id: str
    post_id: str
    content: str
    kind: EngagementType
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class DemoSnapshot:
    post: Post
    engagement: Engagement
    reply: Reply
    guardrails: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)
