# Binox I3 - Mock Content Generation Agent

A mock-first implementation of the Binox I3 take-home task. This project generates stock-market themed content, stores it in a local mock social feed, simulates engagement, and generates contextual replies for questions, compliments, and critiques.

## Release Snapshot (v0.1.0)

- Track: Interns - I3 Content Generation Machine with Reply Capability
- Theme: Stock market speculation watchlist
- Demo mode: Mock social API (no external keys required)
- Orchestration: Local Docker Compose + n8n

## What it does

- Generates themed market-watchlist posts with deterministic templates
- Posts to a local mock X/Twitter adapter instead of the real API
- Simulates common engagement types
- Generates replies with basic guardrails
- Exposes a small HTTP API for n8n to call
- Includes a CLI demo for fast local testing

## Stack

- Python 3.11+
- FastAPI for the local service
- n8n for orchestration
- JSON file storage for the mock social timeline

## Project Structure

- `src/binox_agent/service.py` - HTTP API and browser landing page
- `src/binox_agent/content.py` - content generation logic
- `src/binox_agent/reply.py` - reply classifier and generator
- `src/binox_agent/mock_social.py` - mock posting and engagement storage
- `src/binox_agent/guardrails.py` - safety checks
- `src/binox_agent/cli.py` - local demo command
- `workflows/n8n-stock-loop.json` - starter n8n workflow
- `docker-compose.yml` - local n8n setup
- `architecture.md` - implementation overview
- `evaluation.md` - self-assessment and trade-offs

## Demo Preview

Use the browser demo at `http://localhost:8000/` and click `Run full demo`.

Example response from `/demo/full-loop`:

```json
{
	"post": {
		"content": "Market desk: AI infrastructure is showing a setup worth tracking. Watch the levels, not the noise."
	},
	"replies": [
		{"kind": "question", "reply": "Good question. I'm watching AI infrastructure for confirmation, but I'd treat this as a scenario, not a guarantee."},
		{"kind": "compliment", "reply": "Appreciate it. I'm keeping the thesis simple: track the setup, wait for confirmation, and avoid forcing entries."},
		{"kind": "critique", "reply": "Fair pushback. The point here is to surface a watchlist idea, not claim certainty. I'd rather keep the risk framing explicit."}
	]
}
```

## Setup

1. Create and activate the virtual environment in `.venv`.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the API:

```bash
uvicorn src.binox_agent.service:app --reload
```

4. Run the CLI demo:

```bash
python -m src.binox_agent.cli
```

## Local n8n

Use Docker Compose to run both the API and n8n locally:

```bash
docker compose up --build
```

n8n will be available on `http://localhost:5678`.
The API will be available on `http://localhost:8000`.

## Demo Flow

1. n8n triggers the Python service on a schedule.
2. The service runs the `/demo/full-loop` endpoint.
3. The service generates a stock-themed post.
4. The mock X adapter stores the post locally.
5. Engagement events are created for question, compliment, and critique.
6. The reply engine classifies each message and returns contextual replies.
7. The response is stored back into the mock timeline.

## n8n Starter Workflow

The included `workflows/n8n-stock-loop.json` imports a simple Cron -> HTTP Request flow.
It calls `http://api:8000/demo/full-loop` inside the Compose network, which gives you the full demo loop in one request.

## One-Command Demo

1. Start Docker Desktop.
2. Run `docker compose up --build` in the repo root.
3. Open `http://localhost:8000/docs` to inspect the API.
4. Open `http://localhost:8000/` to use the landing page and run the full demo in-browser.
5. Open `http://localhost:5678` to import the n8n workflow.
6. Trigger the workflow and inspect the JSON response.

## Guardrails

- No spam
- No impersonation
- No guaranteed-profit language
- Rate-limit awareness is documented in the workflow and README
- Mock-only posting by default

## Notes for Submission

For the take-home, this is intentionally mock-first. If you later get API access, the adapter layer in `mock_social.py` can be replaced with a real X/Twitter client without changing the reply logic or workflow structure.
