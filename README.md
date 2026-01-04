# AI Orchestrator Demo

A demo project showcasing a **stateful, AI-ready workflow orchestration engine**
for handling long-running, resumable workflows driven by tickets,
incremental clarifications, structured reasoning, and optional LLM assistance.

The goal of this project is to demonstrate **architecture and orchestration patterns**
rather than model performance or pixel-perfect UI.

---

## Status

✅ **Day 7 complete** — Streaming SOLVING output (presentation-only)
🚧 Ongoing development

### What is implemented

* Backend **workflow orchestration engine** with explicit phases
* Static **ticket catalog** as a controlled workflow entry point
* Deterministic demo domains **and** multiple LLM-backed domains
* LLM integration with:

  * structured JSON prompting
  * retry + semantic validation
  * safe fallbacks
  * token / usage metering
* **Streaming solution generation for SOLVING (LLM domains only)**

  * Server-Sent Events (SSE)
  * incremental Markdown rendering
  * no partial persistence
* Discussion-phase AI chat **with controlled solution refinement**
* Typed React frontend with:

  * catalog-based workflow start
  * workflow list with suspend / resume
  * responsive navigation (drawer on mobile, rail on desktop)
  * dedicated solution panel (not part of chat)
  * optimistic UI for chat and clarification answers
  * discussion chat driving solution updates
  * Markdown rendering for document-style solutions
* Architecture intentionally preserved while adding AI and streaming UX

---

## What This Demo Focuses On

* Stateful, long-lived workflows (not request/response AI calls)
* Explicit workflow phases and transitions
* Incremental clarification gathering (step-by-step, not batch)
* Clear separation of:

  * domain logic
  * orchestration logic
  * infrastructure / adapters
* Intent-based commands instead of generic CRUD
* Persistence designed for suspend / resume / inspect
* Frontend as a **workflow driver**, not just an API client
* Safe integration of probabilistic AI into deterministic control flow
* **Streaming as a presentation concern, not a state concern**

---

## Core Concepts

### Workflow

A **WorkflowState** represents a single, resumable reasoning process.

A workflow progresses through explicit phases:

* `COLLECTING` – gather clarification steps from the user
* `SOLVING` – generate a solution based on collected information
* `DISCUSSION` – optional follow-up discussion with controlled solution refinement
* `DONE` – terminal, immutable state

The workflow engine strictly controls transitions and allowed mutations per phase.

---

### Ticket Catalog

Workflows are started from a **static ticket catalog**, not free-form input.

* Catalog entries define:

  * ticket title and description
  * domain type
  * optional source metadata
* The catalog is **configuration only**
* The engine is unaware of “tickets” as a concept
* The same mechanism is used to launch **reporting workflows**

---

### Clarification Steps

Clarifications are built **incrementally**, one step at a time.

* Each step contains:

  * a prompt
  * an optional answer
  * domain-specific metadata
* Steps may depend on previous answers
* The user may skip directly to solution generation at any time
* Confidence is reported alongside decisions

This mirrors real troubleshooting, reporting, and reasoning workflows.

---

### Streaming Solution Generation (Day 7)

The `SOLVING` phase supports **incremental streaming output** for LLM-backed domains.

Key properties:

* Streaming applies **only** to `SOLVING`
* Streaming is **presentation-only**

  * partial output is never persisted
  * workflow state is updated only once, at completion
* Implemented via **Server-Sent Events (SSE)**
* Backend streams raw Markdown text chunks
* Frontend incrementally renders Markdown in the solution panel
* On completion:

  * streaming state is cleared
  * the workflow is refreshed
  * the persisted final solution replaces streamed content

Deterministic domains and non-streamed paths behave exactly as before.

---

### Discussion & Solution Refinement

The `DISCUSSION` phase enables **controlled refinement** of the solution.

* Users send chat messages only
* The **ChatService** replies and signals intent
* The **SolutionService** may regenerate the solution **as a full replacement**
* Partial or manual solution edits are not allowed
* Each discussion turn produces an explicit outcome (`discussion_result`)

Chat explains *why* the solution changes;
the solution represents the current *truth*.

Streaming does **not** apply to DISCUSSION.

---

### Domain-Driven Orchestration

The engine is **domain-agnostic**.

Domain behavior is plugged in via protocols:

* **StepGenerator** – decides what clarification comes next
* **AnswerParser** – interprets raw user input into domain semantics (optional)
* **SolutionService** – generates a solution or document
* **ChatService** – handles discussion-phase replies (optional)

Domains are registered via a **DomainRegistry** and selected per workflow.

Current demo domains:

* `PRINTER` – deterministic troubleshooting flow (no AI)
* `PARROT` – simple deterministic test domain
* `LLM_SUPPORT` – LLM-backed troubleshooting (clarifications, solution, discussion)
* `LLM_REPORT` – LLM-backed reporting domain producing Markdown documents

LLM-based domains were added **without changing the core engine**.

---

## LLM Integration

LLM usage is integrated safely and intentionally:

* LLM access is abstracted behind an **LLMClient** protocol
* Streaming capability is provided via **StreamingLLMClient**
* Providers (e.g. OpenAI) are isolated in infrastructure adapters
* Structured outputs are enforced via:

  * explicit schemas
  * semantic validation
  * one-retry strict prompting
* Failures degrade gracefully (never crash the engine)

### Token / Cost Metering

* Token usage is captured at the LLM adapter layer
* Prompt + completion tokens are logged per call
* Metering does not leak provider details into domain logic
* Workflow attribution can be added later without refactoring

---

## High-Level Architecture

* **WorkflowState** is the aggregate root
* All mutations go through **WorkflowService**
* Orchestration logic lives in the application layer
* Domain logic is isolated behind protocols
* FastAPI acts as a thin HTTP adapter only
* Persistence is abstracted behind a repository interface
* Workflow state is stored as a snapshot (JSON)

This structure is intentionally designed to evolve toward:

* event-based history
* background execution
* async I/O
* multiple AI providers
* richer UI interactions

---

## Frontend

The frontend is a **typed React application** that drives workflows end-to-end.

Key characteristics:

* No direct backend manipulation
* All interaction goes through intent-based endpoints
* Workflow state is **interpreted**, not mutated, in the UI
* Clear separation between:

  * workflow list
  * active workflow session
  * catalog-based workflow start

### Current UI features

* Start workflows by selecting a predefined **catalog entry**
* Workflow list panel:

  * shows all persisted workflows
  * phase badges for orientation
  * click to suspend / resume
  * responsive (drawer on mobile, rail on desktop)
* Workflow session view:

  * clarification timeline
  * **dedicated solution panel** (sticky, scrollable)
  * **incremental streaming of solutions during SOLVING**
  * Markdown-rendered solutions (including reports)
  * solution confidence display
  * discussion chat below the solution
  * optimistic rendering for user messages and answers
  * explicit “solution updated” indicators
* Multiple workflows can be inspected and resumed freely

The UI is intentionally minimal and optimized for **clarity, calmness, and intent**.

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

* keep domain logic free of event-loop concerns
* minimize accidental complexity

An async repository can be introduced later without changing
domain or orchestration code.

---

## Testing

* Unit tests cover:

  * workflow engine invariants
  * phase transitions
  * deterministic domain behavior
* Tests use in-memory repositories and fake domains
* LLM behavior is validated via schema enforcement and safe fallbacks
* Frontend is tested manually (demo scope)

---

## Why This Design?

This project deliberately avoids a “chatbot-first” architecture.

Instead of treating AI as a stateless function call, the system is built
around **explicit workflows** that model how real problem-solving and
document creation unfold over time.

Key design choices:

* **Workflow as an aggregate**

  * All state lives in one place
  * Easy to inspect, persist, suspend, and resume
* **Explicit phases, procedural engine**

  * Makes orchestration rules visible and testable
  * Avoids implicit state machines hidden in prompts
* **Incremental clarifications**

  * Reflect real troubleshooting and reporting workflows
  * Enable adaptive questioning instead of upfront questionnaires
* **Domain logic behind protocols**

  * Allows deterministic implementations
  * Enables LLM-backed implementations without refactoring
* **Controlled AI integration**

  * AI operates inside strict schemas and engine rules
  * Prevents LLMs from mutating state implicitly
* **Typed frontend as a workflow driver**

  * The UI drives the process intentionally
  * Makes suspend / resume and refinement explicit and visible
* **Streaming as presentation only**

  * Improves UX without weakening correctness or persistence guarantees

Overall, the design favors **clarity, evolvability, and control**
over short-term convenience or raw AI capability.

The current engine is procedural and snapshot-based for clarity.
We already record semantic events, and the next evolution is to let phases emit events instead of mutating state directly. That naturally leads to async execution and background processing.

---

## Limitations (Intentional)

This demo intentionally does **not** include:

* ❌ Authentication / user accounts
* ❌ Multi-tenant isolation
* ❌ Background workers
* ❌ Event sourcing (planned)
* ❌ Automated frontend tests
* ❌ Performance optimizations
* ❌ Pixel-perfect UI
* ❌ Manual document editing

These are excluded to keep the focus on **workflow orchestration,
state management, and architectural clarity**.

---

## Roadmap (Next Steps)

* Read-only review / export views for reports
* Event-based workflow history
* Undo / redo and branching
* Background execution
* Richer discussion controls
* Multiple LLM provider support
* Workflow analytics and cost attribution
