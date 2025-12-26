# AI Orchestrator Demo

A demo project showcasing a **stateful, AI-ready workflow orchestration engine**
for handling long-running, resumable workflows driven by tickets,
clarifications, and structured reasoning.

The goal of this project is to demonstrate **architecture and orchestration patterns**
rather than model performance or UI polish.

---

## Status

✅ **Day 2 complete** — end-to-end orchestration working  
🚧 Ongoing development

- Backend orchestration engine implemented and tested
- Deterministic demo domains (no AI yet)
- Typed frontend driving workflows interactively
- Architecture intentionally frozen before introducing LLMs

---

## What This Demo Focuses On

- Stateful, long-lived workflows (not request/response AI calls)
- Explicit workflow phases and transitions
- Incremental clarification gathering (step-by-step, not batch)
- Clear separation of:
  - domain logic
  - orchestration logic
  - infrastructure / adapters
- Intent-based commands instead of generic CRUD
- Persistence designed for suspend / resume / inspect
- Frontend as a **workflow driver**, not just an API client

---

## Core Concepts

### Workflow

A **WorkflowState** represents a single, resumable reasoning process.

A workflow progresses through explicit phases:

- `COLLECTING` – gather clarification steps from the user
- `SOLVING` – generate a solution based on collected information
- `DISCUSSION` – allow follow-up discussion (UI-ready, AI later)
- `DONE` – terminal state

---

### Clarification Steps

Clarifications are built **incrementally**, one step at a time.

- Each step contains:
  - a prompt
  - an optional answer
  - domain-specific metadata
- Steps may depend on previous answers
- The user may skip directly to solution generation at any time
- Confidence is reported alongside decisions

This mirrors real troubleshooting and reasoning workflows.

---

### Domain-Driven Orchestration

The engine is **domain-agnostic**.

Domain behavior is plugged in via protocols:

- **StepGenerator** – decides what clarification comes next
- **AnswerParser** – interprets raw user input into domain semantics
- **SolveService** – generates a solution draft

Domains are registered via a **DomainRegistry** and selected per workflow.

Current demo domains:
- `PRINTER` – deterministic troubleshooting flow
- `PARROT` – simple test domain that always asks for more info

LLM-based domains will be added later without changing the core engine.

---

## High-Level Architecture

- **WorkflowState** is the aggregate root
- All mutations go through **WorkflowService**
- Orchestration logic lives in the application layer
- Domain logic is isolated behind protocols
- FastAPI acts as a thin HTTP adapter only
- Persistence is abstracted behind a repository interface
- Workflow state is stored as a snapshot (JSON)

This structure is intentionally designed to evolve toward:
- event-based history
- background execution
- async I/O
- multiple AI providers
- richer UI interactions

---

## Frontend

The frontend is a **typed React application** that drives workflows end-to-end.

- No direct backend manipulation
- All interaction goes through intent-based endpoints
- Workflow state is interpreted, not mutated, in the UI
- Minimal Tailwind UI for clarity

The frontend currently supports:
- starting workflows by domain
- answering clarification steps
- skipping to solution
- viewing generated solutions and confidence

The UI is intentionally minimal and optimized for inspection, not polish.

---

## Structure

```
backend/
app/
domain/
application/
api/
tests/

frontend/
src/
api/
data/
components/
types/
```


---

## Persistence

### Database

SQLite is used for simplicity and inspectability.

Each workflow is stored as a single JSON snapshot representing
the current aggregate state.  
This allows easy inspection and prepares the system for
event-based persistence later.

### Sync vs Async

Persistence is currently **synchronous**.

The repository interface is intentionally synchronous to:
- keep domain logic free of event-loop concerns
- minimize accidental complexity

An async repository can be introduced later without changing
domain or orchestration code.

---

## Testing

- Unit tests cover:
  - workflow engine invariants
  - phase transitions
  - deterministic domain behavior
- Tests use in-memory repositories and fake domains
- Frontend is tested manually (demo scope)

---

## Why This Design?

This project deliberately avoids a “chatbot-first” architecture.

Instead of treating AI as a stateless function call, the system is built
around **explicit workflows** that model how real problem-solving unfolds
over time.

Key design choices:

- **Workflow as an aggregate**
  - All state lives in one place
  - Easy to inspect, persist, suspend, and resume
- **Explicit phases**
  - Makes orchestration rules visible and testable
  - Avoids implicit state machines hidden in prompts
- **Incremental clarifications**
  - Reflects real troubleshooting and reasoning
  - Enables adaptive questioning instead of upfront questionnaires
- **Domain logic behind protocols**
  - Allows deterministic implementations today
  - Enables LLM-backed implementations later without refactoring
- **Snapshot-based persistence**
  - Keeps the system simple early on
  - Leaves room for event sourcing when complexity justifies it
- **Typed frontend as a workflow driver**
  - The UI drives the process intentionally
  - Avoids “fire-and-forget” API usage patterns

Overall, the design favors **clarity, evolvability, and control**
over short-term convenience or raw AI capability.

---

## Limitations (Intentional)

This demo intentionally does **not** include:

- ❌ Authentication / user accounts
- ❌ Multi-tenant isolation
- ❌ Background workers
- ❌ Event sourcing (planned)
- ❌ LLM integration (next phase)
- ❌ Performance optimizations
- ❌ Pixel-perfect UI

These are excluded to keep the focus on **workflow orchestration
and architectural clarity**.

---

## Roadmap (Next Steps)

- LLM-based StepGenerator / AnswerParser
- Richer discussion phase
- Chat-like workflow history UI
- Workflow list and resume/suspend UX
- Event-based workflow history
- Background solving execution
