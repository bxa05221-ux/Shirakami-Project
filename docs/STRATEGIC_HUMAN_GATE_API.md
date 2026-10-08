# Strategic Human Gate API Extension v0.1

This additive endpoint exposes the configured Human Gate review profile to an
external client. It does not expose a decision endpoint and does not grant
authority to an AI runtime.

## Endpoint

GET /v1/human-gate/profiles/{profile_id}

The initial profile is `strategic`.

The response contains review requirements and authority invariants, including:

- AI may observe, analyze, and generate options.
- AI may not rank options, select a strategy, or commit a decision.
- Human Gate retains setting confirmation/modification and strategy selection.
- execution, publication, and merge authority remain false.
- Human Gate remains required.

Unknown profiles return HTTP 404.

## Boundary

This is an additive API extension and does not alter the fixed Semantic Handoff
API v1.0 completion boundary. It exposes configuration for human review; it
does not execute a strategy, select a branch, or authorize an action.
