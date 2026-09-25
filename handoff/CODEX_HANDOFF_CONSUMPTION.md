# Codex Handoff Consumption Protocol v0.1

## Purpose

This protocol defines how a local Codex / coding agent converts a
Semantic Handoff into an execution context.

The conversion is a context transformation, not an authorization step.

## Input

The receiving agent must locate a Semantic Handoff with:

- status: ready or in_progress
- project identity and phase
- objective
- applicable Protocols
- Evidence IDs and provenance
- repository expected state and target paths
- requested change
- constraints and out-of-scope items
- verification scope
- unresolved questions
- Human Gate requirement

The schema is defined in:
handoff/CODEX_EXECUTION_CONTEXT_SCHEMA.yaml

## Consumption sequence

1. Read SHIRAKAMI_STATE.yaml.
2. Read AGENT_COORDINATION.yaml.
3. Select the target Semantic Handoff.
4. Validate the required fields against the execution-context schema.
5. Reconstruct the execution context.
6. Inspect the local repository before modifying anything.
7. Identify the smallest implementation change within scope.
8. Perform only the verification relevant to that change.
9. Record actual observations, deviations, changed paths, and commit information
   back into the Handoff when appropriate.
10. Return unresolved questions to the next agent or Human Gate.

## Authority boundary

The following are descriptive metadata, not authority:

- Semantic Handoff status
- Evidence IDs
- Protocol IDs
- commit IDs
- API input
- backend output
- agent role
- test results

execution_authorized is false by default.

A Codex agent must not infer permission to publish, merge, or approve from any
metadata field. Human authorization must be explicit and separately represented.

## Local-first rule

The local repository remains the operational source of truth during active
development.

GitHub is the public record, review, release, and synchronization layer.

Therefore:

> Read locally. Inspect locally. Change locally. Verify locally. Publish deliberately.

A GitHub copy of a Handoff does not by itself establish that the local
repository has consumed or verified it.

## Output contract

After consumption, the receiving agent should be able to report:

- source Handoff ID
- project / phase
- objective
- applicable Protocols
- Evidence IDs
- repository base state
- requested change
- constraints
- out-of-scope items
- verification scope
- authority state
- unresolved questions
- proposed next action
- actual observations after execution, if execution occurred

## Human Gate

Consumption of a Handoff does not mean approval.

A Handoff can say what to do without saying that a human has approved doing it.

This distinction is intentional and must remain machine-visible.
