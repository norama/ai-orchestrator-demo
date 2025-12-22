# AI Orchestrator Demo

A demo project showcasing a stateful AI-assisted workflow engine
integrating external ticket systems and knowledge bases.

## Status

🚧 Work in progress

## Structure

- backend/ – FastAPI backend
- frontend/ – React frontend

## Limitations

- ❌ No auth / user accounts
- ❌ No multi-tenant isolation
- ❌ No background workers (yet)
- ❌ No performance optimization
- ❌ No pixel-perfect UI

## Persistence - database

SQLite is used in this demo.

Persistence is currently synchronous.
The repository interface is intentionally sync to keep the domain and service layers free of event-loop concerns.
An async repository implementation can be introduced later when switching to an async DB driver.