from __future__ import annotations

from dataclasses import asdict
import os
from pathlib import Path
from uuid import uuid4
import json

from .models import Engagement, EngagementType, Post, Reply


class MockSocialClient:
    def __init__(self, storage_path: str | Path = "data/mock_social.json") -> None:
        storage_override = os.getenv("BINOX_STORAGE_PATH")
        self.storage_path = Path(storage_override or storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self._write({"posts": [], "engagements": [], "replies": []})

    def post(self, theme: str, content: str) -> Post:
        post = Post(id=str(uuid4()), theme=theme, content=content)
        data = self._read()
        data["posts"].append(self._serialize(post))
        self._write(data)
        return post

    def add_engagement(self, post_id: str, author: str, text: str) -> Engagement:
        kind = self._guess_kind(text)
        engagement = Engagement(id=str(uuid4()), post_id=post_id, author=author, text=text, kind=kind)
        data = self._read()
        data["engagements"].append(self._serialize(engagement))
        self._write(data)
        return engagement

    def add_reply(self, post_id: str, engagement_id: str, content: str, kind: EngagementType) -> Reply:
        reply = Reply(engagement_id=engagement_id, post_id=post_id, content=content, kind=kind)
        data = self._read()
        data["replies"].append(self._serialize(reply))
        self._write(data)
        return reply

    def get_post_content(self, post_id: str) -> str:
        data = self._read()
        for post in data["posts"]:
            if post["id"] == post_id:
                return post["content"]
        raise KeyError(f"post not found: {post_id}")

    def get_engagement(self, engagement_id: str) -> dict:
        data = self._read()
        for engagement in data["engagements"]:
            if engagement["id"] == engagement_id:
                return engagement
        raise KeyError(f"engagement not found: {engagement_id}")

    def seed_demo_engagements(self, post_id: str) -> list[Engagement]:
        return [
            self.add_engagement(post_id, "marketwatcher", "Why do you like this setup?"),
            self.add_engagement(post_id, "alpha_hunter", "Solid watchlist idea."),
            self.add_engagement(post_id, "risk_first", "I think this is a bit risky, why now?"),
        ]

    def _guess_kind(self, text: str) -> EngagementType:
        lowered = text.lower()
        if any(word in lowered for word in ("risky", "why now", "bad", "weak", "disagree")):
            return EngagementType.CRITIQUE
        if "?" in text:
            return EngagementType.QUESTION
        if any(word in lowered for word in ("nice", "great", "solid", "love")):
            return EngagementType.COMPLIMENT
        return EngagementType.OTHER

    def _read(self) -> dict:
        return json.loads(self.storage_path.read_text(encoding="utf-8"))

    def _write(self, data: dict) -> None:
        self.storage_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _serialize(self, item) -> dict:
        payload = asdict(item)
        for key, value in list(payload.items()):
            if hasattr(value, "isoformat"):
                payload[key] = value.isoformat()
            elif isinstance(value, EngagementType):
                payload[key] = value.value
        return payload
