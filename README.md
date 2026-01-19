# AI Orchestrator Demo

A reference implementation of a **stateful, AI-assisted workflow orchestration engine**.

This project demonstrates how to build AI systems as **long-running, inspectable workflows**
instead of stateless chat interactions.  
AI is treated as a *component inside a controlled process*, not as the process itself.

> This is **not a chatbot demo**.  
> It is an orchestration engine designed for clarity, correctness, and evolvability.

---

## Live Demo

**Try the demo here:**  
**https://ai-orchestrator-demo.vercel.app/**

The demo runs without authentication and supports:
- multiple workflows
- suspend / resume
- history inspection
- snapshot preview
- safe branching
- controlled AI interaction

Each browser session is isolated automatically.

---

## What Problem This Explores

Most AI applications are built as stateless request/response systems.
That model breaks down for real-world use cases such as:

- troubleshooting
- planning
- reporting
- decision support
- document refinement

These activities unfold **over time**, require **incremental clarification**, and benefit from
being **inspectable and resumable**.

This project explores how to design such systems explicitly.

---

## Core Ideas

- **Workflow as the primary abstraction**
  - A workflow represents a single reasoning process
  - It can be suspended, resumed, inspected, and branched
- **Explicit phases**
  - Collect information
  - Generate a solution
  - Refine it through discussion
- **Incremental clarifications**
  - Step-by-step questioning instead of upfront forms
- **Safe AI integration**
  - AI operates inside strict schemas and engine rules
  - No implicit state mutation via prompts
- **History, snapshots, and branching**
  - Past states can be previewed read-only
  - New workflows can be branched safely
- **Streaming as presentation only**
  - Improves UX without weakening correctness or persistence

---

## What This Is (and Is Not)

**This is:**
- an architecture-first demo
- a reference design for AI-assisted workflows
- intentionally explicit and procedural
- focused on clarity over cleverness

**This is not:**
- a production-ready SaaS
- a chatbot wrapper
- an AI prompt playground
- a UI-polish exercise

---

## Documentation

- **Architecture & Design** → [ARCHITECTURE.md](ARCHITECTURE.md)  
  Deep dive into the workflow model, history, snapshots, AI integration, and design rationale.

- **Local Development** → [DEVELOPMENT.md](DEVELOPMENT.md)  
  Tech stack overview, repository structure, and instructions for running the project locally.

---

## Tech Stack (High Level)

- **Backend:** Python, FastAPI, SQLite
- **Frontend:** React, TypeScript, Tailwind
- **AI:** OpenAI API (pluggable)
- **Architecture:** domain-driven orchestration, snapshot-based persistence

---

## Status

This project is actively evolving as an architectural exploration.
Some features are intentionally excluded (auth, background workers, event sourcing)
to keep the focus on **workflow orchestration and state management**.

---

## Why This Exists

Instead of asking *“How do we add AI to an app?”*  
this project asks:

> *“How should we design systems where AI participates in a long-running, inspectable process?”*

The answer is not more prompts — it is **explicit orchestration**.
