# Shirakami Project — Agent Instructions

## Core Principle

AI is a simulator, not an authority.

Human judgment remains the final gate.

## Operational Source

The local repository is the operational source of truth during active development.
GitHub is the public, review, release, and synchronization layer.

## Required State

Read `SHIRAKAMI_STATE.yaml` before making project-level changes.

## Protocol First

Before a consequential change:

1. Identify the applicable Protocol.
2. Identify relevant Evidence IDs.
3. Identify the Semantic Handoff or create one when needed.
4. Define the requested change and verification scope.
5. Implement only within the authorized scope.

## Roles

### ChatGPT

- Project-level reasoning
- Protocol and specification design
- Evidence interpretation
- Semantic Handoff preparation
- Review preparation

### Codex / local coding agent

- Repository inspection
- Implementation
- Local data/code processing
- Tests and verification
- Reporting actual observations and diffs

### GitHub

- Public distribution
- Commit history
- Pull requests
- External review
- Release/reference points

## Verification

Follow the rule:

> 一変更一検証

After modification:

1. Run the relevant verification.
2. Report what was actually observed.
3. Record deviations or failures.
4. Update Evidence or project state when required.

A successful test does not prove the entire Shirakami theory.

## Human Gate

Do not silently:

- redefine project objectives
- change Protocol semantics
- promote an inference to Evidence
- publish or merge a consequential change
- treat AI-generated explanations as authoritative Evidence

Do not push, merge, or publish consequential changes without explicit human authorization.

## Handoff

When work moves between ChatGPT, Codex, the Local Repository, and GitHub, preserve:

- project identity
- current objective
- applicable Protocol
- Evidence IDs
- repository state
- requested change
- verification scope
- unresolved questions

Use the project's Semantic Handoff / 的目YAML conventions.

## Failure and Divergence

If local and GitHub states diverge:

1. Do not silently choose one.
2. Identify the relevant commit/version of each state.
3. Compare changes.
4. Preserve Evidence and Handoff context.
5. Resolve through a human-controlled decision.
6. Re-run verification after reconciliation.

## Scope Discipline

Prefer the smallest change that satisfies the current Handoff.
Do not perform unrelated cleanup merely because it is convenient.
