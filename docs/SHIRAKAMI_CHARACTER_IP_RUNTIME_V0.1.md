# Shirakami Character IP Observation Runtime v0.1

## Purpose

This document defines the minimum runtime contract for using the **白神高校ブラスバンド部** character IP set as observation viewpoints.

Character IPs are not autonomous authorities and are not general-purpose character simulators.

They are bounded observation lenses applied to an existing Context.

## Source world

The initial IP set is derived from the novel **白神高校ブラスバンド部**.

The novel itself contains multiple differentiated viewpoints, parallel dialogue, operational discussion, record keeping, community feedback, and a final transition from meeting records to AI prompts/protocol.

This runtime preserves those distinctions rather than flattening them into a single assistant persona.

## Runtime flow

```
Context
  ↓
Character IP selection
  ↓
Observation
  ↓
Re-expression
  ↓
Human Observation
  ↓
Human Gate
  ↓
Context Update
```

## Character IP contract

Each IP provides:

- identity
- source role
- viewpoint
- characteristic questions
- observation
- uncertainty
- optional proposal

An IP does not provide authority.

## Minimum observation envelope

```yaml
symbolic_observation:
  observation_id: <id>
  source_context_id: <id>

  ip:
    id: <character-ip-id>
    type: named_ip

  observation:
    statement: <observation>

  basis:
    context_refs:
      - <context-ref>

  provenance:
    source_context: existing_context
    symbolic_layer: character_ip
    generated_layer: ai_interpretation

  uncertainty:
    - <uncertainty>

  proposal:
    statement: <optional-proposal>

  authority:
    character_ip: none
    human_gate: required

  context_update:
    allowed: false
```

## Authority rule

Character IP output MUST NOT directly mutate canonical Context.

The following path is prohibited:

```
Character IP
    ↓
Canonical Context
```

The required path is:

```
Character IP
    ↓
Observation
    ↓
Human Observation
    ↓
Human Gate
    ↓
Canonical Context
```

## Multi-IP observation

Multiple IPs may observe the same Context independently.

Their outputs MUST remain distinguishable.

```
             ┌─ 黒滝一郎
             ├─ ヲタコン
Context ─────┼─ 元山くん
             ├─ 八重樫さん
             ├─ みさき
             ├─ 菅原先生
             └─ 校長
                    ↓
             observations
                    ↓
              human review
```

The purpose is not to make the IPs agree.

The purpose is to expose differences in observation.

## Provenance rule

The runtime MUST preserve the distinction between:

1. source Context;
2. source-derived material;
3. character-IP observation;
4. AI-generated re-expression;
5. human-approved Context update.

Invoking a character IP does not create evidence.

## V0.2 acceptance test

The minimum implementation passes when:

1. a Context is supplied;
2. one character IP observes it;
3. the observation retains provenance;
4. the observation is presented to a Human Gate;
5. acceptance can update canonical Context;
6. rejection cannot update canonical Context.

No additional character simulation features are required for this boundary.
