# Shirakami Project

## A Language Protocol OS for Keeping AI Under Human Direction

Shirakami Project is a research, design, and implementation project focused not on making AI itself smarter, but on creating an environment in which people can use AI according to their own intentions.

Shirakami Model does not replace the LLM itself. It structures human language, treats it as a Language Protocol, and creates an explicit structure between people and AI Runtime so that collaboration with AI remains controllable from the human side.

> **AI is a simulator, not an authority.**
>
> AI is not the final decision-maker; it is a simulator that supports human judgment.

---

## Landscape

Shirakami Project is not a single application. It separates research, meaning, specification, implementation, and applications while preserving their relationships.

```text
                 Shirakami Project
                        │
        ┌───────────────┼───────────────┐
        │               │               │
     Research         Model        Specification
        │               │               │
   Theory / Ideas   Language Protocol    Specification
        │               OS               │
        └───────────────┼───────────────┘
                        │
                     Runtime
                        │
                  AI / Application
                        │
                    Evidence
                        │
                 Human Judgment
```

### Repository roles

| Repository | Role |
|---|---|
| [`shirakami-research`](https://github.com/bxa05221-ux/shirakami-research) | Theory, hypotheses, and research experiments |
| [`shirakami-model`](https://github.com/bxa05221-ux/shirakami-model) | Shirakami Model / Language Protocol OS |
| [`shirakami-specification`](https://github.com/bxa05221-ux/shirakami-specification) | Protocol, structure, and specification |
| [`shirakami-OS`](https://github.com/bxa05221-ux/shirakami-OS) | Runtime, implementation, and tests |

Related application and experimental repositories are connected according to their respective responsibilities.

---

## Basic Structure

Shirakami is organized around the following flow:

```text
Human Language
      ↓
Prompt Organization
      ↓
Language Protocol
      ↓
Computational Task
      ↓
AI Runtime
      ↓
Evidence / Observation
      ↓
Human-readable Options
      ↓
Human Judgment
```

The essential principle is **not to make AI output the final decision**.

Shirakami treats AI output as material for human judgment and aims to structurally distinguish confirmed information, estimates, interpretations, and creative elements.

---

## Language Protocol OS

Shirakami Model is a **Language Protocol OS** designed to support the structured handling of language protocols.

It organizes human prompts, expands them into forms that AI can process, and treats them as computational tasks.

It also aims to adapt to user-specific Language Protocols by observing language use, patterns of thought, and phrasing.

This does not improve the intrinsic capability of an AI model itself.

**The goal is to improve the human experience of using AI, rather than the intelligence of AI itself.**

---

## Evidence

In AI interaction, confirmed information can become mixed with estimates, interpretations, and creative elements.

Shirakami treats deviations of meaning and related uncertainty as Evidence, aiming to distinguish confirmed information from unconfirmed elements.

This helps prevent AI output from being treated automatically as fact or as a final decision.

---

## Human Judgment

The center of Shirakami is not AI, but the human.

Rather than assuming that AI should lead the task, Shirakami can present multiple perspectives and options and return the final judgment to the human.

```text
AI → Proposal / Simulation / Organization
                 ↓
              Human
                 ↓
          Judgment / Decision
```

---

## Semantic Handoff

To prevent project separation from severing meaning, Shirakami Project uses **Matome YAML (的目YAML)** as the formal semantic handoff unit.

```text
Mother
  ↓
Research
  ↓
Matome YAML
  ↓
Local Repository
  ↓
Verification
  ↓
GitHub
  ↓
Operation
  ↓
Evidence
  ↓
Mother
```

ChatGPT Projects may be used as working spaces, but conversation history itself is not treated as the sole source of truth.

- **Matome YAML** — semantic handoff
- **Local Repository** — development state
- **GitHub Repository** — confirmed implementation and history
- **Mother** — overall Landscape and coordination

This separation keeps research and implementation distinct while preserving meaning and history.

---

## Development Status

Shirakami is currently in a shakedown phase toward operational use.

This does not declare a finished product or a finished theory.

Findings from implementation, verification, and operation are treated as Evidence / Findings and may be returned to Research for reconsideration.

**One change, one verification.**

---

## Start Here

For a first look at Shirakami, the following order is recommended:

1. **Model** — What Shirakami is intended to achieve
2. **Specification** — How its structures are defined
3. **OS / Runtime** — How those structures are implemented
4. **Research** — The theories, hypotheses, and experiments behind them

---

## Core Principle

> **Do not make AI smarter.**  
> **Make it possible for people to use AI on their own terms.**

---

## Project Status

**Prototype / β1.0 Operational Rollout**

Shirakami Project is an ongoing landscape of research, specification, implementation, and applications.
