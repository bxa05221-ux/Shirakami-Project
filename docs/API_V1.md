# Shirakami API v1.0

## Purpose

Shirakami API v1.0 exposes the existing Semantic Handoff boundary through a
real HTTP transport without changing the authority model.

The transport is deliberately thin:

```
External Client
      |
      | HTTP GET
      v
Shirakami HTTP Transport
      |
      v
ShirakamiAPI
      |
      v
Semantic Handoff
```

The HTTP layer is not a decision layer and does not grant authority.

## Endpoint

`GET /v1/semantic-handoff/{trace_id}`

Required query parameters:

- `project`
- `objective`
- `protocol_ids` (may be repeated)
- `verification_scope`

Optional:

- `activity_id`

The response preserves lineage fields and explicitly retains:

- `execution_authorized: false`
- `publish_authorized: false`
- `merge_authorized: false`
- `human_gate_required: true`
- `decision_authority: false`

Unknown traces return HTTP 404. Missing required parameters return HTTP 400.

## Local demonstration

The transport uses only Python's standard library. No web framework is
required for the v1.0 boundary.

A minimal server can be created with:

```python
from runtime.api import ShirakamiAPI
from runtime.http_api import create_server

api = ShirakamiAPI(traces)
server = create_server(api, host="127.0.0.1", port=8000)
server.serve_forever()
```

For an externally visible deployment, place the same boundary behind the
deployment's normal process manager or HTTP gateway. Deployment, authentication,
TLS, rate limiting, and production operations are outside the fixed v1.0 core
conformance scope.

## Completion boundary

API v1.0 is complete when the following are green:

1. real HTTP endpoint
2. connection to the existing Semantic Handoff core
3. authority invariance across HTTP
4. Evidence / provenance preservation
5. runtime/provider compatibility already covered by the existing adapter gate
6. external-client HTTP E2E
7. minimal safe failures
8. reproducible GitHub Actions conformance

No additional test dimensions are required for the v1.0 completion claim.
