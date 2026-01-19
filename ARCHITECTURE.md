# Architecture & Design

This document describes the **architectural design and core concepts**
behind the **AI Orchestrator Demo**.

The goal is to explain *how* the system works and *why* it is designed this way,
with a focus on **workflow orchestration, state management, and safe AI integration**.

This is a **reference architecture**, not a production-ready blueprint.

---

## Design Overview

The system is built around a single central idea:

> **AI-assisted problem solving should be modeled as an explicit, long-running workflow.**

Instead of treating AI as a stateless request/response function, this project models
reasoning as a process that:
- unfolds over time
- requires incremental clarification
- must be inspectable and resumable
- can safely branch into alternative paths

The architecture prioritizes:
- explicit state
- visible transitions
- controlled side effects
- evolvability over cleverness

---

## Workflow Model

A **workflow** represents a single reasoning or problem-solving process.

It is the primary aggregate and unit of persistence.

### Workflow Phases

Each workflow progresses through explicit phases:

- **COLLECTING**  
  Incrementally gather clarification steps from the user.

- **SOLVING**  
  Generate a solution based on collected information.

- **DISCUSSION**  
  Optional follow-up discussion with controlled solution refinement.

- **DONE**  
  Terminal, immutable state.

Transitions between phases are explicitly controlled by the engine.
Each phase defines which operations are allowed.

---

## Ticket Catalog

Workflows are started from a **static ticket catalog**.

Key properties:

- Tickets define:
  - title
  - description
  - domain type
  - optional source metadata
- The catalog is **configuration only**
- The workflow engine is unaware of “tickets” as a concept
- The same mechanism is used to launch reporting workflows

This avoids free-form prompts as workflow entry points and keeps workflow creation intentional.

---

## Clarification Steps

Clarifications are gathered **incrementally**, one step at a time.

Each clarification step contains:
- a prompt
- an optional answer
- domain-specific metadata

Important properties:

- Steps may depend on previous answers
- Domains decide which clarification comes next
- Users may skip directly to solution generation
- Confidence is tracked alongside decisions

This mirrors real troubleshooting, planning, and reporting workflows.

---

## Workflow History & Snapshots

Workflows expose a **read-only history timeline** composed of semantic events.

### Snapshots

- Snapshots represent **immutable workflow states**
- Only user-visible waiting states create snapshots
- One snapshot is always designated as the **current (live)** snapshot

Each history event references:
- a snapshot ID
- the previous snapshot ID

History is **explanatory**, not controlling.

---

## Snapshot Preview

Any snapshot can be loaded in **preview mode**:

- Workflow state is rendered read-only
- All mutating actions are disabled
- UI clearly distinguishes preview vs live mode

From preview mode, the user may:
- return to the live workflow
- branch a new workflow

Preview is treated as navigation, not state mutation.

---

## Branching

A new workflow can be **branched from any snapshot**.

Branching behavior:

- Creates a new workflow ID
- Preserves:
  - parent workflow ID
  - parent snapshot ID
- Starts from the selected snapshot state
- Leaves the parent workflow unchanged

This enables safe experimentation and alternative solution paths.

---

## Streaming Solution Generation

The **SOLVING** phase supports incremental streaming output for LLM-backed domains.

Key rules:

- Streaming applies **only** to SOLVING
- Streaming is **presentation-only**
- Partial output is never persisted
- Workflow state is updated once, at completion

Implementation details:

- Server-Sent Events (SSE)
- Backend streams raw Markdown chunks
- Frontend incrementally renders Markdown
- Final persisted solution replaces streamed content

Deterministic domains behave identically without streaming.

---

## Discussion & Solution Refinement

The **DISCUSSION** phase enables controlled refinement of the solution.

Rules:

- Users send chat messages only
- Chat replies explain intent and reasoning
- The solution may be regenerated as a **full replacement**
- Partial or manual edits are not allowed

Each discussion turn produces an explicit outcome.
The solution always represents the current source of truth.

Streaming does **not** apply to DISCUSSION.

---

## Domain-Driven Orchestration

The engine itself is **domain-agnostic**.

Domain behavior is plugged in via protocols:

- **StepGenerator**  
  Decides which clarification step comes next

- **AnswerParser** (optional)  
  Interprets raw user input into domain semantics

- **SolutionService**  
  Generates a solution or document

- **ChatService** (optional)  
  Handles discussion-phase replies

Domains are registered via a **DomainRegistry**.

### Demo Domains

- **PRINTER** – deterministic troubleshooting (no AI)
- **PARROT** – deterministic test domain
- **LLM_SUPPORT** – AI-assisted troubleshooting
- **LLM_REPORT** – AI-assisted reporting (Markdown documents)

LLM-backed domains were added **without changing the core engine**.

---

## LLM Integration

LLM usage is intentionally constrained.

Key principles:

- LLM access is abstracted behind an **LLMClient** protocol
- Streaming is provided via **StreamingLLMClient**
- Providers are isolated in infrastructure adapters
- Structured outputs are enforced via:
  - explicit schemas
  - semantic validation
  - one-retry strict prompting
- Failures degrade gracefully

### Token & Cost Metering

- Token usage is captured at the adapter layer
- Prompt and completion tokens are logged per call
- Metering does not leak provider details into domain logic

---

## High-Level Architecture

- **WorkflowState** is the aggregate root
- All mutations go through **WorkflowService**
- Orchestration logic lives in the application layer
- Domain logic is isolated behind protocols
- FastAPI acts as a thin HTTP adapter
- Persistence is abstracted behind a repository interface
- Workflow state is stored as immutable snapshots (JSON)

The architecture is designed to evolve toward:
- event-sourced persistence
- background execution
- async workflows
- multiple AI providers

---

## Frontend Architecture

The frontend is a **typed React application** that drives workflows end-to-end.

Key properties:

- No direct backend manipulation
- All interaction goes through intent-based endpoints
- Workflow state is interpreted, not mutated, in the UI
- Clear separation between:
  - workflow list
  - active workflow session
  - catalog-based workflow start

The UI is intentionally minimal and optimized for **clarity and intent**.

---

## Persistence Model

- SQLite is used for simplicity and inspectability
- Persistence is currently synchronous
- Repository interfaces are intentionally synchronous
- Storage includes:
  - current workflow snapshot
  - semantic workflow events
  - snapshot lineage

The snapshot-based model prepares the system for event sourcing later.

---

## Intentional Limitations

This demo intentionally does **not** include:

- Authentication or user accounts
- Multi-tenant isolation
- Background workers
- Event sourcing (planned)
- Automated frontend tests
- Performance optimizations
- Manual document editing

These are excluded to keep focus on **workflow orchestration and state management**.

---

## Design Rationale

This project deliberately avoids a “chatbot-first” architecture.

Instead of asking:
> “How do we add AI to an app?”

it asks:
> “How do we design systems where AI participates in a long-running, inspectable process?”

The answer is **explicit orchestration**, not more prompts.

The current engine is procedural and snapshot-based for clarity.
Semantic events are already recorded; the next evolution is to let phases emit events instead of mutating state directly.
This naturally leads to async execution and background processing.

---

## Roadmap

- Read-only review / export views
- Event-sourced persistence
- Undo / redo
- Background execution
- Richer history diffing
- Workflow analytics and cost attribution
