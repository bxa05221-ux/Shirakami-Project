# Shirakami v0.2 — Symbolic Recursion Scope

## Purpose

V0.2 extends the completed v0.1 Context/authority foundation with **Symbolic Recursion**: the ability to re-observe an existing Context through another symbolic system or observation subject, then return the resulting observation to Context.

## Core loop

Context → Symbol / IP → Observation → Re-expression → Human Observation → Context Update

## Definitions

- **Symbol**: a person, fictional character, work, proverb, maxim, metaphor, setting, or other symbolic system used as an observation lens.
- **IP**: a defined observation subject/persona. An anonymous IP may be user-defined rather than tied to a known character.
- **Symbolic Recursion**: mapping Context into a symbolic lens, generating an observation/re-expression through that lens, and preserving the distinction between source Context, symbolic interpretation, and newly observed output.
- **Provenance**: records whether a statement is a verified fact, direct quotation, attributed hearsay, work-derived material, or AI-generated interpretation.

## Invariants

1. Symbolic interpretation MUST NOT become factual evidence merely because a symbol was invoked.
2. A fictional or anonymous IP MUST NOT acquire authority over the Human Gate.
3. Provenance MUST survive the symbolic boundary.
4. Re-expression MUST remain distinguishable from the source Context.
5. Human observation remains the final authority for Context updates.
6. V0.2 MUST reuse the v0.1 authority, verification, and Semantic Handoff boundaries rather than replacing them.

## Initial scope

1. Minimal Symbolic Recursion protocol envelope.
2. Provenance-aware Symbol/IP representation.
3. One end-to-end re-observation path.
4. Human Gate compatibility.
5. Verification that symbolic output cannot directly mutate canonical Context.

## Explicitly out of scope

- General-purpose character simulation.
- Autonomous agents with independent authority.
- Copyright corpus ownership or bulk collection.
- Production deployment hardening.
- Kodama/proactive ubiquitous interaction.
- Full radio/manga/media pipelines.

## Stop condition

V0.2 initial implementation is complete when one symbolic observation can traverse the declared boundary, preserve provenance, pass Human Gate, and demonstrate that rejected symbolic output cannot mutate canonical Context.

Further symbolic variants are not added unless they expose a concrete violation of these invariants.
