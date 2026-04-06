# Self-Assessment

## What Works Well

- The demo is deterministic, which makes it reliable during review.
- The mock API pattern keeps the system safe and easy to run locally.
- The reply engine covers the three required engagement types.
- The Docker Compose setup supports a one-command local run.

## Trade-offs

- The content generation is template-driven rather than model-generated.
- The engagement simulator is intentionally simple and not a real social listener.
- The n8n workflow is a starter flow, not a full production automation graph.

## Next Improvements If More Time Is Available

- Add persistence queries and a simple history view for posts/replies.
- Add richer prompt variants or an optional LLM adapter.
- Expand the n8n workflow to separate posting, monitoring, and reply stages.
