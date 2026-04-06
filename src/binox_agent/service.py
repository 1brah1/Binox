from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .content import ContentGenerator, ThemeSpec
from .guardrails import Guardrails
from .mock_social import MockSocialClient
from .models import Engagement, EngagementType
from .reply import ReplyEngine

app = FastAPI(title="Binox I3 Mock Content Agent", version="0.1.0")

THEME = ThemeSpec(
    name="stock-speculation-watchlist",
    voice="Market desk",
    topics=["large-cap momentum", "earnings rebound", "AI infrastructure", "energy rotation", "small-cap breakouts"],
    call_to_action="Watch the levels, not the noise.",
)

_guardrails = Guardrails()
_content_generator = ContentGenerator(THEME, _guardrails)
_reply_engine = ReplyEngine(_guardrails)
_social_client = MockSocialClient()


class GenerateRequest(BaseModel):
    seed: int | None = None


class EngageRequest(BaseModel):
    post_id: str = Field(min_length=1)
    author: str = Field(min_length=1)
    text: str = Field(min_length=1)


class ReplyRequest(BaseModel):
    post_id: str = Field(min_length=1)
    engagement_id: str = Field(min_length=1)


LANDING_PAGE = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Binox I3 Demo</title>
    <style>
        :root {
            color-scheme: dark;
            --bg: #0b0f14;
            --panel: #121824;
            --panel-2: #172033;
            --text: #e6edf7;
            --muted: #9fb0c6;
            --accent: #5eead4;
            --accent-2: #f59e0b;
            --border: rgba(255,255,255,.08);
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Inter, Segoe UI, Arial, sans-serif;
            background:
                radial-gradient(circle at top left, rgba(94, 234, 212, 0.12), transparent 30%),
                radial-gradient(circle at top right, rgba(245, 158, 11, 0.10), transparent 28%),
                linear-gradient(180deg, #06080c 0%, var(--bg) 100%);
            color: var(--text);
            min-height: 100vh;
        }
        .wrap {
            max-width: 1120px;
            margin: 0 auto;
            padding: 40px 20px 56px;
        }
        .hero {
            display: grid;
            grid-template-columns: 1.1fr .9fr;
            gap: 20px;
            align-items: start;
        }
        .card {
            background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 18px 60px rgba(0,0,0,.35);
            backdrop-filter: blur(10px);
        }
        h1 {
            margin: 0 0 12px;
            font-size: clamp(2.2rem, 5vw, 4.2rem);
            line-height: 1;
            letter-spacing: -0.04em;
        }
        .eyebrow {
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: .16em;
            font-size: .76rem;
            font-weight: 700;
            margin-bottom: 16px;
        }
        p, li, pre {
            color: var(--muted);
            line-height: 1.55;
        }
        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin: 22px 0 0;
        }
        .btn {
            appearance: none;
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 12px 16px;
            background: rgba(255,255,255,.04);
            color: var(--text);
            cursor: pointer;
            font-weight: 600;
            text-decoration: none;
        }
        .btn.primary { background: linear-gradient(135deg, var(--accent), #60a5fa); color: #041016; border: 0; }
        .btn:hover { transform: translateY(-1px); }
        .grid {
            margin-top: 20px;
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px;
        }
        .metric {
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 16px;
            background: rgba(255,255,255,.02);
        }
        .metric strong {
            display: block;
            margin-bottom: 8px;
            color: #fff;
        }
        pre {
            margin: 0;
            background: #0a0f17;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 16px;
            overflow-x: auto;
            min-height: 280px;
            white-space: pre-wrap;
            word-break: break-word;
        }
        .section-title {
            margin: 0 0 12px;
            font-size: 1rem;
            color: #fff;
        }
        @media (max-width: 900px) {
            .hero, .grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="wrap">
        <div class="hero">
            <section class="card">
                <div class="eyebrow">Binox I3 demo</div>
                <h1>Stock watchlist agent with reply capability</h1>
                <p>
                    This mock-first prototype generates a themed market post, stores it in a local social feed,
                    and replies to common engagement types with guardrails.
                </p>
                <div class="actions">
                    <button class="btn primary" id="run-demo">Run full demo</button>
                    <a class="btn" href="/docs" target="_blank" rel="noreferrer">Open API docs</a>
                </div>
                <div class="grid">
                    <div class="metric"><strong>Theme</strong><span>Stock speculation / watchlist</span></div>
                    <div class="metric"><strong>Engagements</strong><span>Question, compliment, critique</span></div>
                    <div class="metric"><strong>Workflow</strong><span>Python API + n8n orchestration</span></div>
                </div>
            </section>
            <section class="card">
                <h2 class="section-title">Live demo output</h2>
                <pre id="output">Click "Run full demo" to generate a sample loop.</pre>
            </section>
        </div>
    </div>
    <script>
        const output = document.getElementById('output');
        document.getElementById('run-demo').addEventListener('click', async () => {
            output.textContent = 'Running demo...';
            try {
                const response = await fetch('/demo/full-loop', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ seed: 7 })
                });
                const data = await response.json();
                output.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                output.textContent = 'Demo failed: ' + error;
            }
        });
    </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def landing_page() -> str:
        return LANDING_PAGE


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate-post")
def generate_post(request: GenerateRequest) -> dict[str, str]:
    content = _content_generator.generate(request.seed)
    post = _social_client.post(THEME.name, content)
    return {"post_id": post.id, "theme": post.theme, "content": post.content}


@app.post("/mock/engagement")
def create_engagement(request: EngageRequest) -> dict[str, str]:
    engagement = _social_client.add_engagement(request.post_id, request.author, request.text)
    return {
        "engagement_id": engagement.id,
        "post_id": engagement.post_id,
        "author": engagement.author,
        "text": engagement.text,
        "kind": engagement.kind.value,
    }


@app.post("/reply")
def reply(request: ReplyRequest) -> dict[str, str]:
    engagement_data = _social_client.get_engagement(request.engagement_id)
    engagement = Engagement(
        id=engagement_data["id"],
        post_id=engagement_data["post_id"],
        author=engagement_data["author"],
        text=engagement_data["text"],
        kind=EngagementType(engagement_data["kind"]),
    )
    post_text = _social_client.get_post_content(request.post_id)
    plan = _reply_engine.generate_reply(engagement, post_text)
    reply = _social_client.add_reply(request.post_id, engagement_data["id"], plan.response, plan.kind)
    return {
        "reply_id": reply.engagement_id,
        "kind": reply.kind.value,
        "content": reply.content,
    }


@app.post("/demo/full-loop")
def full_loop(request: GenerateRequest) -> dict:
    content = _content_generator.generate(request.seed)
    post = _social_client.post(THEME.name, content)
    engagements = _social_client.seed_demo_engagements(post.id)
    replies = []
    for engagement in engagements[:3]:
        plan = _reply_engine.generate_reply(engagement, post.content)
        reply = _social_client.add_reply(post.id, engagement.id, plan.response, plan.kind)
        replies.append({"engagement_id": engagement.id, "reply": reply.content, "kind": plan.kind.value})
    return {"post": {"id": post.id, "content": post.content}, "engagements": [e.text for e in engagements], "replies": replies}
