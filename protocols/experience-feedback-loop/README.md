# Experience Feedback Loop

Experimental protocol for turning real execution outcomes into reusable Shirakami evidence without granting authority to any AI runtime.

## Core idea

Multiple runtimes may attempt the same task. Shirakami records what happened, what was verified, what failed, and what humans corrected. Those observations can generate **protocol candidates**.

A candidate is not a rule until a human reviews and approves it.

```text
Task
  ↓
Context → Protocol
  ↓
Multiple Runtimes
  ↓
Execution
  ↓
Observation / Evidence
  ↓
Verification
  ↓
Human Review
  ↓
Protocol Candidate
  ↓
Human Gate
  ↓
Controlled Update
  ↓
Next Execution
```

## Why failures matter

A failed execution is not discarded. It becomes reusable evidence when its failure mode, verification status, and any human correction are recorded.

The protocol therefore follows:

> Success produces evidence. Failure produces evidence. Human correction produces evidence.

None of these automatically becomes truth.

## Multi-runtime comparison

The protocol does **not** rank models globally. It compares evidence for a defined task and context.

This allows ECC, Codex, and other runtimes to coexist as replaceable execution mechanisms while Shirakami retains the protocol and human-control layer.

## Authority boundary

- Runtime: execution authority only.
- AIwitness: observation and execution-fact recording only.
- Evidence: supports reasoning but has no authority.
- Protocol candidate: unverified until reviewed.
- Human Gate: required before consequential protocol or policy changes.

## Relationship to Shirakami

This protocol is intentionally kept as a separate experimental line. It can later be connected to Semantic Handoff, Evidence IDs, AIwitness, and Runtime adapters after independent testing.
