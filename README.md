# AI Orchestrator Demo

A demo project showcasing a **stateful, AI-ready workflow orchestration engine**
for handling long-running, resumable workflows driven by tickets,
clarifications, structured reasoning, and optional LLM assistance.

The goal of this project is to demonstrate **architecture and orchestration patterns**
rather than model performance or UI polish.

---

## Status

✅ **Day 3 complete** — AI-ready orchestration with conversational UI  
🚧 Ongoing development

### What is implemented

- Backend **workflow orchestration engine** with explicit phases
- Deterministic demo domains **and** LLM-backed domain
- LLM integration with:
  - structured JSON prompting
  - retry + validation
  - safe fallbacks
  - token / usage metering
- Discussion-phase AI chat (non-mutating)
- Typed React frontend with:
  - chat-style workflow display
  - workflow list
  - suspend / resume across workflows
- Architecture intentionally preserved while adding AI

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
- Safe integration of probabilistic AI into deterministic control flow

---

## Core Concepts

### Workflow

A **WorkflowState** represents a single, resumable reasoning process.

A workflow progresses through explicit phases:

- `COLLECTING` – gather clarification steps from the user
- `SOLVING` – generate a solution based on collected information
- `DISCUSSION` – optional follow-up discussion (LLM-powered)
- `DONE` – terminal, immutable state

The workflow engine strictly controls transitions between phases.

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
- **SolutionService** – generates a solution draft
- **ChatService** – handles discussion-phase replies (optional)

Domains are registered via a **DomainRegistry** and selected per workflow.

Current demo domains:

- `PRINTER` – deterministic troubleshooting flow (no AI)
- `PARROT` – simple deterministic test domain
- `LLM_SUPPORT` – fully LLM-backed clarification, solution, and discussion

LLM-based domains were added **without changing the core engine**.

---

## LLM Integration

LLM usage is integrated safely and intentionally:

- LLM access is abstracted behind an **LLMClient** protocol
- Providers (e.g. OpenAI) are isolated in infrastructure adapters
- Structured JSON outputs are enforced via:
  - explicit schemas
  - semantic validation
  - one-retry strict prompting
- Failures degrade gracefully (never crash the engine)

### Token / Cost Metering

- Token usage is captured at the LLM adapter layer
- Prompt + completion tokens are logged per call
- Metering does not leak provider details into domain logic
- Workflow attribution can be added later without refactoring

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

Key characteristics:

- No direct backend manipulation
- All interaction goes through intent-based endpoints
- Workflow state is **interpreted**, not mutated, in the UI
- Clear separation between:
  - workflow list (catalog)
  - active workflow session
  - UI navigation state

### Current UI features

- Start workflows with configurable:
  - domain
  - name
  - description
  - max clarification steps
- Chat-style workflow display:
  - AI prompts
  - user answers
  - solution rendering with confidence
  - discussion-phase chat
- Workflow list panel:
  - shows all persisted workflows
  - ordered by recent activity
  - click to suspend / resume
- Multiple workflows can be inspected and resumed freely

The UI is intentionally minimal and optimized for clarity, not polish.

---

## Structure

```
backend/
app/
domain/
application/
api/
infrastructure/
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
- LLM behavior is validated via schema enforcement and safe fallbacks
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
  - Allows deterministic implementations
  - Enables LLM-backed implementations without refactoring
- **Controlled AI integration**
  - AI operates inside strict schemas and engine rules
  - Prevents LLMs from mutating state implicitly
- **Typed frontend as a workflow driver**
  - The UI drives the process intentionally
  - Makes suspend / resume explicit and visible

Overall, the design favors **clarity, evolvability, and control**
over short-term convenience or raw AI capability.

---

## Limitations (Intentional)

This demo intentionally does **not** include:

- ❌ Authentication / user accounts
- ❌ Multi-tenant isolation
- ❌ Background workers
- ❌ Event sourcing (planned)
- ❌ Automated frontend tests
- ❌ Performance optimizations
- ❌ Pixel-perfect UI

These are excluded to keep the focus on **workflow orchestration,
state management, and architectural clarity**.

---

## Roadmap (Next Steps)

- Event-based workflow history
- Undo / redo and branching
- Solution revision commands
- Background execution
- Richer discussion controls
- Multiple LLM provider support
- Workflow analytics and cost attribution
