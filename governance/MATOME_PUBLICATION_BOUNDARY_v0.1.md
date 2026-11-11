# Matome YAML Publication Boundary v0.1

## Purpose

This document defines the publication boundary for the Shirakami Matome YAML library.

The Matome YAML format and its public semantic contracts may be published. The detailed design history that led to those contracts is treated separately.

> **Publish the meaning and the contract. Protect the design path and sensitive evidence.**

## Public by default

The following may be published when they contain no case-specific confidential data:

- Matome YAML schema and field definitions
- public examples and templates
- core principles
- Human Gate and human-authority rules
- Runtime replaceability
- Provider-neutrality and anti-lock-in boundaries
- Evidence semantics and verification states
- Semantic Handoff contracts
- public adapter and runtime interfaces
- public architectural diagrams
- public implementation necessary to reproduce the documented contract
- public, non-sensitive verification records

These materials explain **what Shirakami is and how its public contract behaves**.

## Protected by default

The following are not part of the public Matome specification unless deliberately released as a separate publication:

- detailed development chronology
- exploratory design notes
- failed experiments and abandoned alternatives
- internal reasoning that led from one design decision to another
- unpublished implementation strategies
- unreleased product or commercialization plans
- operational know-how learned from private deployments
- private Context or Evidence
- personal information
- credentials, API keys, tokens, secrets, or private infrastructure details
- confidential partner or customer information
- unpublished research results

These materials describe **how the design was discovered, refined, or operationalized**, rather than the public contract itself.

## Design-history boundary

A public Matome may state a principle such as:

> AI is a simulator/reasoning component, not the final authority.

It does not need to disclose the complete sequence of experiments, failures, prompts, observations, and design decisions that produced that principle.

Likewise, a public Semantic Handoff specification may define what must be preserved across a handoff without publishing every internal experiment that established why those fields were selected.

## Evidence boundary

Evidence has two publication classes.

### Public Evidence

Evidence deliberately prepared as a reproducible public example or verification record.

### Protected Evidence

Runtime observations, logs, Context, user data, internal experiments, or operational records whose disclosure is not necessary to understand the public contract.

A public Matome MUST NOT be interpreted as authorization to publish all Evidence associated with it.

## Historical repositories and prior commits

This policy does not claim that a public repository can retroactively make previously published Git history private.

If sensitive design-history material has already been published, it should be reviewed separately and, where appropriate, moved out of the public distribution path in a deliberate repository-history/privacy operation.

Deleting a file from the current tree does not by itself erase its historical availability.

## Publication rule

Before adding material to the public Matome library, classify it as one of:

- `public-contract`
- `public-example`
- `public-verification`
- `protected-design-history`
- `protected-operational`
- `protected-sensitive-data`

Only the first three are public-library defaults.

## Important distinction

This is a publication and information-management rule. It is not a legal determination that a particular item is patentable, a trade secret, copyrighted, or otherwise legally protected.

---

**Short form**

> **的目YAMLの仕様は公開する。  
> 的目YAMLに入る実データは分類する。  
> 成立過程・設計知・未公開運用知は、別の保護層として扱う。**
