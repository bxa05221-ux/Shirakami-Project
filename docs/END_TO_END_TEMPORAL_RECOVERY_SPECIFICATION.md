# End-to-End Temporal + Recovery Integrity v0.1

## Purpose

This test composes three protections:

1. temporal integrity prevents stale, replayed, or out-of-order authority;
2. decision binding prevents approval reuse outside its exact scope;
3. persistence/recovery integrity prevents an interrupted transition from
   becoming a new authority source.

## Composed invariant

> Recovery, mutation, or temporal disorder must never increase runtime authority.

## Acceptance criteria

A complete chain may pass only when:

- the event graph is causally valid;
- execution matches the exact human-approved context, evidence, protocol, and proposal;
- persisted state is known and approval-bound;
- runtime authority is not asserted.

The suite injects one failure at each boundary and requires the complete
chain to fail closed.

A committed state is reconciled; it is not treated as permission to execute
again. An interrupted state is quarantined for re-verification.

## Non-claim

This is a deterministic integrity test, not proof that every possible
distributed-system failure has been modeled. Real process, storage, and
network failures remain future test surfaces.
