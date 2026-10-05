# Shirakami API v0.1

## Purpose

Provide a provider-neutral HTTP transport around the existing Shirakami API
boundary without moving authority into the Runtime.

## v0.1 surface

- GET /health — transport health only.
- GET /v1/capabilities — reports available API capabilities.
- GET /v1/semantic-handoff/{trace_id} — retrieves an existing Semantic Handoff.
- POST requests are intentionally rejected by the first transport prototype.

## Authority boundary

The HTTP layer does not authorize execution, publication, or merge.

Human Gate remains an external authority boundary. Mutation endpoints will only
be added after an E2E test demonstrates that the same Human Gate and Verification
invariants are preserved through the API.

## Local run

From the repository root:

    python -m api.http_server

The default listener is 127.0.0.1:8787.

This is a transport prototype, not a production deployment.
