# Shirakami Persistence / Recovery Integrity Specification v0.1

## Purpose

A restart, crash, rollback, or incomplete transition must never create new
decision authority.

## Rule

Only a known durable state may resume, and resumption must revalidate the
human approval against the exact Context, Evidence, Protocol, and Proposal
binding.

## Fail-closed states

The following states are quarantined:

- unknown
- apply_started
- crashed
- incomplete

The recovery action for these states is quarantine_and_reverify.

## Durable states

The following states may request recovery after integrity validation:

- approved
- candidate_created
- verified
- committed

This specification does not treat persistence as proof of human authority.
Persistence only preserves a previously established authority boundary.

## Required invariants

- A restart cannot manufacture approval.
- A crash cannot convert uncertainty into execution authority.
- A persisted approval cannot be rebound to another Context.
- Evidence, Protocol, and Proposal bindings cannot be swapped after restart.
- Runtime authority claims remain forbidden during recovery.
