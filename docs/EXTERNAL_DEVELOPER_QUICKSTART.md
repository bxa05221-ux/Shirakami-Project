# External Developer Quickstart

This is the shortest path for an independent developer to inspect and run the
existing Shirakami API v1.0 boundary.

## 1. What you are looking at

Shirakami is **not an LLM** and the API is not a decision endpoint.

The relevant boundary is:

```
External Client
    ↓ HTTP
Shirakami HTTP Transport
    ↓
Semantic Handoff
    ↓
Evidence / Lineage
    ↓
Human Gate
```

The runtime may produce proposals or simulation results, but the API does not
turn those results into execution, publication, or merge authority.

For the API boundary, these values remain false:

- `execution_authorized`
- `publish_authorized`
- `merge_authorized`

Human Gate remains required and final.

## 2. Requirements

- Python 3.11 or newer
- Git

No web framework is required for the API v1.0 demo.

## 3. Run the local HTTP demo

From the repository root:

```bash
python examples/api-v1-server.py
```

In another terminal:

```bash
python examples/api-v1-client.py http://127.0.0.1:8000 TRACE-HTTP-001
```

The response should show the trace/handoff/evidence lineage and the
authority fields above.

The server uses a deterministic local fixture. It does not call an external
AI provider.

## 4. Verify the boundary yourself

Run the existing focused HTTP test:

```bash
python -m pytest scripts/test_api_http.py -q
```

Then run the fixed API v1.0 conformance gate:

```bash
python scripts/run_api_conformance.py
```

These checks cover the already-defined API v1.0 boundary. They are not an
invitation to expand the v1.0 test program.

## 5. Where to read next

- `docs/API_V1.md` — API boundary and completion scope
- `runtime/http_api.py` — thin HTTP transport
- `runtime/api.py` — provider-neutral API facade
- `examples/api-v1-client.py` — external client
- `scripts/test_api_http.py` — executable HTTP boundary evidence
- `docs/CORE_CONFORMANCE.md` — core authority-preservation gate
- `protocols/reviewer-protocol-v0.1.md` — broader reviewer path

## 6. What is deliberately not here

API v1.0 does **not** claim to be a production hosting solution.

Authentication, TLS, rate limiting, deployment operations, and JOUMON/v2 are
separate future work. They are not prerequisites for reviewing or using this
local handoff boundary.

## 7. The Human Gate rule

If an implementation appears to let an AI/runtime/API select or authorize an
action, that is a boundary violation, not a feature to work around.

The governing principle is:

> **AI is a simulator, not an authority.**

A reviewer should be able to verify that principle from the code and tests
without requiring a live explanation from the author.
