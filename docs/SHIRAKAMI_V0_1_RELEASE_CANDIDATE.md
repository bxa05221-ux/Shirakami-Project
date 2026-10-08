# Shirakami v0.1 Release Candidate Boundary

## Purpose

This document freezes the completion boundary for Shirakami v0.1 and prevents additional edge-case work from silently expanding the milestone.

## Candidate base

- Base commit: 47d22b655859a052d7f2468803ad703b794a0b4d
- Candidate branch: release/shirakami-v0.1-candidate

The candidate base contains the verified v0.1 implementation line through API v1.0 and the strategic Human Gate extension.

## v0.1 completion boundary

The following are treated as complete for v0.1:

- Core authority chain
- Human Gate
- Verification / forgery resistance
- Runtime / Adapter boundary
- AIwitness decision-map boundary
- API v1.0 HTTP boundary
- External developer handoff
- ThreadRPG historical / derived-core mapping

## Explicitly not required for v0.1

- ThreadRPG as a dedicated Runtime
- Symbolic Recursion
- Anonymous IP
- Symbolic retrieval
- Kodama / proactive ubiquitous interaction
- Production hosting, TLS, rate limiting, or deployment hardening
- Additional verification variants that do not demonstrate a broken v0.1 invariant

## v0.1 stop rule

Once the candidate passes the existing conformance and authority-chain verification already associated with the completed milestones, new edge cases are not added to v0.1 unless they demonstrate a concrete violation of a declared v0.1 invariant.

## v0.2 boundary

v0.2 begins a separate research/implementation line:

Context -> Symbol / IP -> Observation -> Re-expression -> Human Observation -> Context Update

Its initial scope is Symbolic Recursion, provenance-aware IP, and context re-observation.

## Canonicalization task

Before calling v0.1 the repository-level release, reconcile this candidate with the current `main` branch so that the public default branch and the release candidate do not silently represent different completion states.

This is a repository canonicalization task, not a new architecture feature.
