# Matome YAML → Semantic Handoff: Lineage Boundary v0.1

Status: research record / bounded architecture finding
Date: 2026-10-08

## 1. Purpose

This record isolates the remaining question from the ThreadRPG lineage work:

> What, exactly, survived from Matome YAML into the later Semantic Handoff boundary?

The goal is to establish a defensible lineage without falsely treating every historical Matome field as a current normative Runtime field.

## 2. Finding

The lineage is **semantic, not schema-identical**.

Matome YAML originated as a human-authored state/context handoff representation. The later Semantic Handoff boundary generalizes the same continuity requirement into an explicit boundary between external observation/context and Runtime execution.

Therefore:
- Matome YAML is an historical/source representation;
- Protocol IR is an implementation representation for executable Protocols;
- Semantic Handoff is a boundary contract for preserving explicitly supplied meaning, identity, provenance, and uncertainty across system boundaries;
- no current evidence establishes that Semantic Handoff is a direct field-for-field successor schema to Matome YAML.

This distinction should remain explicit.

## 3. Historical Matome evidence

The historical ThreadRPG Matome example contains:
- protocol identity (title, version);
- human-readable statement;
- declared pipeline phases.

The published ThreadRPG description additionally describes Matome YAML as carrying forward:
- state;
- observation;
- interpretation;
- uncertainty;
- unresolved items;
- next observation.

The historical repository also records a stronger architectural observation:

Root Evidence → Dialogue / Observation → Difference (Delta) → Matome YAML

That record explicitly treats Matome YAML as a derived representation rather than the source of record.

## 4. Later Protocol boundary

The historical Protocol specification defines:

Matome YAML → Protocol Loader → Protocol IR → Runtime → Evidence → Landscape State

It identifies Matome YAML as the canonical human-authored representation for Protocol definitions, while treating Protocol IR as an implementation artifact.

This establishes a second role for Matome:
1. preserving/handoff of context;
2. authoring/serialization of Protocol definitions.

Those roles must not be conflated.

## 5. Later Semantic Handoff boundary

The historical Semantic Handoff boundary defines a different, narrower responsibility:

Landscape Observation → External API → External Client / Runtime

Its minimum envelope preserves:
- landscape_id;
- explicit protocol_id when supplied;
- generated observation_id;
- state/result;
- evidence identity;
- provenance.

It explicitly forbids authority creation and rejects implicit execution/approval semantics.

Its key invariant is:

> APIは意味を渡すが、権限を作らない。

This is not a replacement for the entire Matome representation. It is a boundary discipline derived from the same context-continuity problem.

## 6. Lineage map

| Historical Matome concern | Later generalized boundary | Status |
|---|---|---|
| Preserve context/state | Landscape / Context / Semantic Handoff | strong continuity |
| Preserve observation | Observation envelope / Evidence | strong continuity |
| Preserve interpretation as distinguishable information | Evidence / interpretation separation | conceptual continuity |
| Preserve uncertainty | explicit uncertainty preservation | strong continuity |
| Preserve unresolved items | Evidence / unresolved state | conceptual continuity |
| Preserve next observation | verification / re-observation loop | strong continuity |
| Preserve protocol identity | explicit protocol_id reference | implemented |
| Preserve provenance | provenance + evidence identity | implemented |
| Prevent handoff from becoming authority | forbidden authority fields / Human Gate boundary | implemented and verified |
| Serialize executable Protocol structure | Matome → Protocol IR | historically implemented |
| Preserve exact historical Matome schema | current Semantic Handoff | **not established** |

## 7. Architectural conclusion

The safe statement is:

> **Semantic Handoff is the generalized boundary discipline that emerged from the earlier Matome/context-continuity problem; it is not proven to be a direct successor schema of Matome YAML.**

This is sufficient for the ThreadRPG → Shirakami lineage.

The architecture does not need to reintroduce the historical Matome schema into the Runtime merely to preserve ancestry.

## 8. Remaining design question

The only genuinely new schema question is:

> What is the smallest canonical semantic handoff object that preserves the Shirakami invariant without importing historical Matome fields that are no longer required?

That question should be answered from current verified boundaries, not by reconstructing every historical Matome variant.

A reasonable minimum candidate is:

landscape reference + observation identity + explicit protocol reference (optional) + observable state/result + evidence identity + provenance + uncertainty

Authority/approval/execution identity remains outside the observational handoff unless an explicitly governed Human Gate contract supplies it.

## 9. Stop condition

This lineage task is complete when:
1. Matome is documented as historical/source representation;
2. Semantic Handoff is documented as generalized boundary discipline;
3. no field-for-field ancestry is claimed without evidence;
4. current Runtime does not acquire historical Matome complexity solely for compatibility;
5. any future canonical handoff schema is defined as a new, bounded architecture decision.

No new Runtime implementation is justified by this finding alone.