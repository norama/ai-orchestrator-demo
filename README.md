# AI Orchestrator Demo

A demo project showcasing a **stateful AI-assisted workflow engine**
for handling long-running, resumable workflows driven by tickets,
clarifications, and AI-assisted reasoning.

The goal of this project is to demonstrate **architecture and orchestration patterns**
rather than model performance or UI polish.

---

## Status

🚧 Work in progress (Day 1: foundation)

---

## What This Demo Focuses On

- Stateful, long-lived workflows (not request/response AI calls)
- Explicit workflow phases and transitions
- Clear separation of domain, application, and infrastructure layers
- Intent-based commands instead of generic CRUD updates
- Persistence designed for suspend / resume / inspect

---

## High-Level Architecture

- **WorkflowState** is the aggregate root
- All mutations go through a **WorkflowService**
- FastAPI acts as a thin HTTP adapter only
- Persistence is abstracted behind a repository interface
- The current workflow state is stored as a snapshot (JSON)

This structure is intentionally designed to evolve toward:
- Event-based history
- Background execution
- Async I/O
- Multiple AI providers

---

## Structure

- `backend/` – FastAPI backend (clean architecture)
- `frontend/` – React frontend (minimal, demo-only)

---

## Persistence

### Database

SQLite is used in this demo for simplicity and inspectability.

Workflow state is stored as a single JSON snapshot per workflow.
This reflects the current aggregate state and allows easy evolution
toward event-based persistence later.

### Sync vs Async

Persistence is currently **synchronous**.

The repository interface is intentionally sync to keep the domain
and service layers free of event-loop concerns and to minimize
accidental complexity at this stage.

An async repository implementation can be introduced later
when switching to an async DB driver (e.g. async Postgres),
without changing the domain model.

---

## Limitations (Intentional)

This demo intentionally does **not** include:

- ❌ Authentication / user accounts
- ❌ Multi-tenant isolation
- ❌ Background workers (yet)
- ❌ Event sourcing (planned)
- ❌ Performance optimizations
- ❌ Pixel-perfect UI

These are excluded to keep the focus on **workflow orchestration
and architectural clarity**.

---

## Roadmap (Short-Term)

- AI-generated clarification questions
- Phase-driven orchestration logic
- Background execution for solving phase
- Optional event-based workflow history
