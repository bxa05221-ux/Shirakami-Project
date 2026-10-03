# JOUMON Runtime Substitution Experiment v0.1

## Question

Can the same Context and Protocol be executed through different Runtime
implementations while preserving the semantic and authority boundary?

## Controlled variables

Keep constant:

- Context ID
- Context task
- Context constraints
- Protocol ID
- Human final-decision authority
- Human Gate requirement

Allow to vary:

- Runtime ID
- Provider identity
- Runtime output
- Runtime-specific implementation

## Experiment

The deterministic PoC runs one shared contract through:

1. Sakana Fugu-shaped runtime boundary
2. Alternate runtime boundary

The Fugu-shaped runtime is not a live Sakana API call. It is a deterministic
test double using the same adapter boundary that a later live integration can
use.

## Expected invariant

```
Context + Protocol + Human Gate
            |
            +------ Runtime A
            |
            +------ Runtime B
```

Changing the Runtime must not change:

- the Context identity;
- the Protocol identity;
- the declaration that final decision authority is human;
- the requirement for Human Gate;
- the evidence lineage relationship.

Changing the Runtime may change:

- output;
- runtime identity;
- provider metadata;
- execution-specific evidence.

## Interpretation

A passing deterministic test demonstrates only that the JOUMON implementation
can preserve these declared invariants under Runtime substitution.

It does **not** demonstrate:

- equivalent model quality;
- equivalent factual accuracy;
- live provider behavior;
- production readiness;
- superiority of Sakana Fugu or any other runtime.

The next validation layer is a live, credentialed execution followed by
cross-runtime Evidence comparison.
