# Shirakami Core Conformance

## Purpose

Core Conformance is the minimum regression gate for the Shirakami authority-preservation core.

It is intentionally narrower than the full regression suite.

## Required invariants

- Verification PASS does not imply authorization.
- AI/runtime output cannot become human authority.
- Mutation, provenance, and identity changes fail closed.
- Human Gate remains the final authority.
- Runtime replacement cannot transfer authority.

## Gate

The executable gate is:

`python scripts/run_core_conformance.py`

The runner currently selects 13 authority-preservation test modules, including verification integrity/forgery, verifier authenticity/provenance, independent verification, cross-layer authority, Human Gate and identity/authentication, decision replay/binding, end-to-end integrity, and the Full-System Authority Chain.

## Status rule

This document defines the gate; it does not by itself certify a commit.

A commit may be described as **Core Conformance GREEN** only after the GitHub Actions workflow `Shirakami Core Conformance` completes successfully for that commit.

Until then, the state is **CONFORMANCE PENDING**.
