from __future__ import annotations

from .content import ContentGenerator, ThemeSpec
from .guardrails import Guardrails
from .mock_social import MockSocialClient
from .reply import ReplyEngine


def main() -> None:
    theme = ThemeSpec(
        name="stock-speculation-watchlist",
        voice="Market desk",
        topics=["large-cap momentum", "earnings rebound", "AI infrastructure", "energy rotation", "small-cap breakouts"],
        call_to_action="Watch the levels, not the noise.",
    )
    guardrails = Guardrails()
    generator = ContentGenerator(theme, guardrails)
    reply_engine = ReplyEngine(guardrails)
    social = MockSocialClient()

    post_text = generator.generate(seed=7)
    post = social.post(theme.name, post_text)
    engagements = social.seed_demo_engagements(post.id)

    print(f"POST [{post.id}] {post.content}")
    for engagement in engagements:
        plan = reply_engine.generate_reply(engagement, post.content)
        social.add_reply(post.id, engagement.id, plan.response, plan.kind)
        print(f"ENGAGEMENT [{engagement.kind.value}] {engagement.author}: {engagement.text}")
        print(f"REPLY: {plan.response}")
