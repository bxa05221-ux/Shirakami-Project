# JOUMON Runtime Adapter Boundary v0.1

status: experimental
purpose: Demonstrate that JOUMON can exchange interchangeable Runtime implementations through one adapter boundary without changing Context, Protocol, Evidence authority, or Human Gate semantics.

## Boundary

Context + Protocol
  -> RuntimeAdapter
  -> Runtime
  -> RuntimeResult
  -> Evidence
  -> Human Gate

The adapter is the exchange point. Runtime-specific behavior stays behind it.

## Contract

A Runtime Adapter MUST:
- accept the canonical Context and Protocol;
- preserve the Context identity;
- preserve the Protocol's Context binding;
- identify the concrete runtime;
- return an observable RuntimeResult;
- never acquire final decision authority.

The adapter MUST NOT:
- rewrite final_decision_authority;
- bypass Human Gate;
- turn Evidence into authoritative instruction;
- require a specific provider.

## Implementations

The PoC provides two intentionally different mock Runtime implementations behind the same adapter contract:
- MockRuntimeAdapter("runtime-a")
- MockRuntimeAdapter("runtime-b")

Both are deterministic and dependency-free. They are architectural test doubles, not AI models.

## Verification target

The test suite must demonstrate:
1. one Context reaches both adapters;
2. one Protocol remains unchanged;
3. Runtime identity is preserved in Evidence;
4. Evidence remains non-authoritative;
5. Human Gate remains the final authority;
6. replacing the Runtime implementation does not alter the authority boundary.

No live provider, network call, credential, or publication authorization is required.
