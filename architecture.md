# Architecture

## Overview

Binox I3 is implemented as a mock-first content generation agent with a small FastAPI service, a JSON-backed social feed adapter, and a local n8n workflow.

## Components

- `src/binox_agent/content.py` generates stock-themed posts using a deterministic theme spec.
- `src/binox_agent/mock_social.py` stores posts, engagements, and replies in a JSON file.
- `src/binox_agent/reply.py` classifies engagement text and generates contextual replies.
- `src/binox_agent/guardrails.py` prevents spammy or unsafe language from being emitted.
- `src/binox_agent/service.py` exposes the HTTP API and the browser landing page.
- `workflows/n8n-stock-loop.json` demonstrates the scheduled automation flow.

## Runtime Flow

1. n8n triggers the `/demo/full-loop` endpoint on a schedule or manual run.
2. The API generates a post and writes it to the mock social store.
3. The mock adapter creates sample engagement events.
4. The reply engine classifies each engagement and returns a response.
5. The response is stored back into the local mock timeline.

## Why This Shape

- It is easy to demo without any external keys.
- It keeps X/Twitter integration behind a swappable adapter.
- It keeps orchestration separate from the core content logic.
- It makes the submission reproducible on a clean machine.
