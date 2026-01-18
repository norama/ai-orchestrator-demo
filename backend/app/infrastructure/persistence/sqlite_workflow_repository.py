import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import override
from uuid import UUID, uuid4

from app.application.exceptions import SnapshotNotFound, SnapshotWorkflowMismatch, WorkflowNotFound
from app.domain.config import DomainType
from app.domain.event import (
    EVENT_DATA_MODELS,
    WorkflowEvent,
    WorkflowEventCreate,
)
from app.domain.ticket import Ticket
from app.domain.workflow import (
    Workflow,
    WorkflowState,
)
from app.infrastructure.persistence.workflow_repository import (
    WorkflowRepository,
)

DB_PATH = "app/infrastructure/persistence"


class SqliteWorkflowRepository(WorkflowRepository):
    def __init__(self, workspace_name: str = "ai_orchestrator"):
        self.db_path = os.path.join(DB_PATH, f"{workspace_name}.db")
        self._last_ts: datetime | None = None

        self._ensure_db()

    def _ensure_db(self) -> None:
        Path(self.db_path).touch(exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS workflows (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    max_steps INTEGER NOT NULL,
                    ticket_json TEXT NOT NULL,
                    domain_type TEXT NOT NULL CHECK (domain_type IN ('PARROT', 'PRINTER', 'LLM_SUPPORT', 'LLM_REPORT')),
                    current_snapshot_id TEXT NOT NULL,
                    parent_id TEXT NULL,
                    parent_snapshot_id TEXT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

            conn.execute("""
            CREATE TABLE IF NOT EXISTS workflow_snapshots (
                id TEXT PRIMARY KEY,
                workflow_id TEXT NOT NULL,
                state_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """)

            conn.execute("""
            CREATE TABLE IF NOT EXISTS workflow_events (
                id TEXT PRIMARY KEY,
                workflow_id TEXT NOT NULL,
                snapshot_id TEXT NOT NULL,
                previous_snapshot_id TEXT NULL,
                type TEXT NOT NULL CHECK (type IN ('WORKFLOW_CREATED', 'WORKFLOW_BRANCHED', 'CLARIFICATION_UPDATED', 'SOLUTION_GENERATED', 'CHAT_REPLIED', 'SOLUTION_UPDATED', 'WORKFLOW_COMPLETED')),
                data_json TEXT NULL,
                created_at TEXT NOT NULL
            )
            """)
            conn.commit()

    def _create_snapshot(
        self,
        conn: sqlite3.Connection,
        workflow_id: UUID,
        *,
        state: WorkflowState,
        created_at: datetime,
    ) -> UUID:
        snapshot_id = uuid4()

        conn.execute(
            """
            INSERT INTO workflow_snapshots (id, workflow_id, state_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                str(snapshot_id),
                str(workflow_id),
                state.model_dump_json(),
                created_at.isoformat(),
            ),
        )

        return snapshot_id

    def _create_event(
        self,
        conn: sqlite3.Connection,
        workflow_id: UUID,
        *,
        previous_snapshot_id: UUID | None = None,
        snapshot_id: UUID,
        event_create: WorkflowEventCreate,
        created_at: datetime,
    ) -> UUID:
        event_id = uuid4()

        model = EVENT_DATA_MODELS.get(event_create.type)
        validated_data = model.model_validate(event_create.data) if model and event_create.data else None

        conn.execute(
            """
            INSERT INTO workflow_events (id, workflow_id, snapshot_id, previous_snapshot_id, type, data_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(event_id),
                str(workflow_id),
                str(snapshot_id),
                str(previous_snapshot_id) if previous_snapshot_id else None,
                event_create.type.value,
                validated_data.model_dump_json() if validated_data else None,
                created_at.isoformat(),
            ),
        )

        return event_id

    def _next_created_at(self) -> datetime:
        now = datetime.now(timezone.utc)

        if self._last_ts is None:
            ts = now
        else:
            ts = max(now, self._last_ts + timedelta(microseconds=1))

        self._last_ts = ts
        return ts

    def _create_snapshot_with_events(
        self,
        conn: sqlite3.Connection,
        workflow_id: UUID,
        *,
        state: WorkflowState,
        previous_snapshot_id: UUID | None = None,
        events: list[WorkflowEventCreate] | None = None,
    ) -> UUID:
        snapshot_id = self._create_snapshot(conn, workflow_id, state=state, created_at=datetime.now(timezone.utc))

        if events:
            for event in events:
                self._create_event(
                    conn,
                    workflow_id,
                    previous_snapshot_id=previous_snapshot_id,
                    snapshot_id=snapshot_id,
                    event_create=event,
                    created_at=self._next_created_at(),
                )

        return snapshot_id

    @override
    def insert_workflow(self, workflow: Workflow, events: list[WorkflowEventCreate] | None = None) -> Workflow:
        with sqlite3.connect(self.db_path) as conn:
            now = datetime.now(timezone.utc)
            workflow.updated_at = now
            current_snapshot_id = self._create_snapshot_with_events(
                conn,
                workflow.id,
                state=workflow.state,
                events=events,
            )

            conn.execute(
                """
                INSERT INTO workflows (id, name, description, max_steps, ticket_json, domain_type, current_snapshot_id, parent_id, parent_snapshot_id, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(workflow.id),
                    workflow.name,
                    workflow.description,
                    workflow.max_steps,
                    workflow.ticket.model_dump_json(),
                    workflow.domain_type.value,
                    str(current_snapshot_id),
                    str(workflow.parent_id) if workflow.parent_id else None,
                    str(workflow.parent_snapshot_id) if workflow.parent_snapshot_id else None,
                    workflow.updated_at.isoformat(),
                ),
            )
            conn.commit()

        return workflow

    @override
    def get_workflow(self, workflow_id: UUID) -> Workflow | None:
        with sqlite3.connect(self.db_path) as conn:
            cursor_w = conn.execute(
                """
                SELECT
                    w.id,
                    w.name,
                    w.description,
                    w.max_steps,
                    w.ticket_json,
                    w.domain_type,
                    w.parent_id,
                    w.parent_snapshot_id,
                    w.updated_at,
                    ws.state_json
                FROM workflows w
                JOIN workflow_snapshots ws
                    ON ws.id = w.current_snapshot_id
                WHERE w.id = ?
                """,
                (str(workflow_id),),
            )
            row_w = cursor_w.fetchone()

            if row_w is None:
                return None

            (
                id,
                name,
                description,
                max_steps,
                ticket_json,
                domain_type,
                parent_id,
                parent_snapshot_id,
                updated_at,
                state_json,
            ) = row_w

            if row_w is None:
                return None

        return Workflow(
            id=UUID(id),
            name=name,
            description=description,
            max_steps=max_steps,
            ticket=Ticket.model_validate_json(ticket_json),
            domain_type=DomainType(domain_type),
            updated_at=datetime.fromisoformat(updated_at),
            parent_id=UUID(parent_id) if parent_id else None,
            parent_snapshot_id=UUID(parent_snapshot_id) if parent_snapshot_id else None,
            state=WorkflowState.model_validate_json(state_json),
        )

    @override
    def get_workflows(self) -> list[Workflow]:
        workflows: list[Workflow] = []

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                 SELECT
                    w.id,
                    w.name,
                    w.description,
                    w.max_steps,
                    w.ticket_json,
                    w.domain_type,
                    w.parent_id,
                    w.parent_snapshot_id,
                    w.updated_at,
                    ws.state_json
                FROM workflows w
                JOIN workflow_snapshots ws
                    ON ws.id = w.current_snapshot_id
                ORDER BY w.updated_at DESC
                """
            )
            rows = cursor.fetchall()

        for row in rows:
            (
                id,
                name,
                description,
                max_steps,
                ticket_json,
                domain_type,
                parent_id,
                parent_snapshot_id,
                updated_at,
                state_json,
            ) = row

            workflow = Workflow(
                id=UUID(id),
                name=str(name) if name is not None else None,
                description=str(description) if description is not None else None,
                max_steps=max_steps,
                ticket=Ticket.model_validate_json(ticket_json),
                domain_type=DomainType(domain_type),
                updated_at=datetime.fromisoformat(updated_at),
                parent_id=UUID(parent_id) if parent_id else None,
                parent_snapshot_id=UUID(parent_snapshot_id) if parent_snapshot_id else None,
                state=WorkflowState.model_validate_json(state_json),
            )
            workflows.append(workflow)

        return workflows

    @override
    def get_snapshot(self, workflow_id: UUID, snapshot_id: UUID) -> WorkflowState:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT
                    workflow_id as snapshot_workflow_id,
                    state_json
                FROM workflow_snapshots
                WHERE id = ?
                LIMIT 1
                """,
                (str(snapshot_id),),
            )
            row = cursor.fetchone()

        if row is None:
            raise SnapshotNotFound(f"Snapshot with ID {snapshot_id} does not exist")

        (
            snapshot_workflow_id,
            state_json,
        ) = row

        if UUID(snapshot_workflow_id) != workflow_id:
            raise SnapshotWorkflowMismatch(
                f"Snapshot {snapshot_id} does not belong to workflow {workflow_id} but to workflow {snapshot_workflow_id}"
            )

        return WorkflowState.model_validate_json(state_json)

    @override
    def update_workflow(self, workflow: Workflow, events: list[WorkflowEventCreate] | None = None) -> Workflow:
        previous_snapshot_id = self.get_current_snapshot_id(workflow.id)

        with sqlite3.connect(self.db_path) as conn:
            now = datetime.now(timezone.utc)
            workflow.updated_at = now
            current_snapshot_id = self._create_snapshot_with_events(
                conn,
                workflow.id,
                state=workflow.state,
                previous_snapshot_id=previous_snapshot_id,
                events=events,
            )

            conn.execute(
                """
                UPDATE workflows
                SET current_snapshot_id = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    str(current_snapshot_id),
                    workflow.updated_at.isoformat(),
                    str(workflow.id),
                ),
            )
            conn.commit()

        return workflow

    @override
    def get_events(self, workflow_id: UUID) -> list[WorkflowEvent]:
        events: list[WorkflowEvent] = []

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT
                    e.id,
                    e.workflow_id,
                    e.snapshot_id,
                    e.previous_snapshot_id,
                    e.type,
                    e.data_json,
                    e.created_at
                FROM workflow_events e
                WHERE e.workflow_id = ?
                ORDER BY e.created_at ASC
                """,
                (str(workflow_id),),
            )
            rows = cursor.fetchall()

        for row in rows:
            (
                id,
                workflow_id,
                snapshot_id,
                previous_snapshot_id,
                type,
                data_json,
                created_at,
            ) = row

            model = EVENT_DATA_MODELS.get(type)
            if model is None and data_json is not None:
                raise ValueError(f"Event type {type} should not have data")
            if model is not None and data_json is None:
                raise ValueError(f"Event type {type} requires data")

            data = model.model_validate_json(data_json) if model else None

            event = WorkflowEvent(
                id=UUID(id),
                workflow_id=workflow_id,
                snapshot_id=UUID(snapshot_id),
                previous_snapshot_id=UUID(previous_snapshot_id) if previous_snapshot_id else None,
                type=type,
                data=data.model_dump() if data else None,
                created_at=datetime.fromisoformat(created_at),
            )

            events.append(event)

        return events

    @override
    def get_current_snapshot_id(self, workflow_id: UUID) -> UUID:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT current_snapshot_id
                FROM workflows
                WHERE id = ?
                """,
                (str(workflow_id),),
            )
            row = cursor.fetchone()

            if row is None:
                raise WorkflowNotFound(f"Cannot get current snapshot ID: workflow with ID {workflow_id} does not exist")

            (current_snapshot_id,) = row

        return UUID(current_snapshot_id)
