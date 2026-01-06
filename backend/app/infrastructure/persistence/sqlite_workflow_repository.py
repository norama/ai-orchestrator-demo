import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import override
from uuid import UUID, uuid4

from app.application.exceptions import SnapshotNotFound, WorkflowNotFound
from app.domain.config import DomainType
from app.domain.ticket import Ticket
from app.domain.workflow import (
    Workflow,
    WorkflowCreate,
    WorkflowHistory,
    WorkflowHistoryItem,
    WorkflowPhase,
    WorkflowState,
)
from app.infrastructure.persistence.workflow_repository import (
    WorkflowRepository,
)

DB_PATH = "app/infrastructure/persistence/ai_orchestrator.db"


class SqliteWorkflowRepository(WorkflowRepository):
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

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
            conn.commit()

    def _create_snapshot(
        self,
        conn: sqlite3.Connection,
        workflow_id: UUID,
        state: WorkflowState,
        created_at: datetime,
    ) -> str:
        snapshot_id = str(uuid4())

        conn.execute(
            """
            INSERT INTO workflow_snapshots (id, workflow_id, state_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                snapshot_id,
                str(workflow_id),
                state.model_dump_json(),
                created_at.isoformat(),
            ),
        )

        return snapshot_id

    def persist(self, workflow: Workflow) -> Workflow:
        with sqlite3.connect(self.db_path) as conn:
            now = datetime.now(timezone.utc)
            workflow.updated_at = now
            current_snapshot_id = self._create_snapshot(conn, workflow.id, workflow.state, now)

            conn.execute(
                """
                INSERT INTO workflows (id, name, description, max_steps, ticket_json, domain_type, current_snapshot_id, parent_id, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(workflow.id),
                    workflow.name,
                    workflow.description,
                    workflow.max_steps,
                    workflow.ticket.model_dump_json(),
                    workflow.domain_type.value,
                    current_snapshot_id,
                    str(workflow.parent_id) if workflow.parent_id else None,
                    workflow.updated_at.isoformat(),
                ),
            )
            conn.commit()

        return workflow

    @override
    def create(self, workflow_create: WorkflowCreate) -> Workflow:
        workflow = Workflow(**workflow_create.model_dump())

        return self.persist(workflow)

    @override
    def get(self, workflow_id: UUID) -> Workflow | None:
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
                    w.updated_at,
                    ws.state_json
                FROM workflows w
                JOIN workflow_snapshots ws
                    ON ws.id = w.current_snapshot_id
                WHERE w.id = ?
                """,
                (str(workflow_id),),
            )
            row = cursor.fetchone()

        if row is None:
            return None

        (
            id,
            name,
            description,
            max_steps,
            ticket_json,
            domain_type,
            parent_id,
            updated_at,
            state_json,
        ) = row

        return Workflow(
            id=UUID(id),
            name=name,
            description=description,
            max_steps=max_steps,
            ticket=Ticket.model_validate_json(ticket_json),
            domain_type=DomainType(domain_type),
            updated_at=datetime.fromisoformat(updated_at),
            parent_id=UUID(parent_id) if parent_id else None,
            state=WorkflowState.model_validate_json(state_json),
        )

    @override
    def list(self) -> list[Workflow]:
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
                updated_at,
                state_json,
            ) = row

            workflow = Workflow(
                id=UUID(id),
                name=name,
                description=description,
                max_steps=max_steps,
                ticket=Ticket.model_validate_json(ticket_json),
                domain_type=DomainType(domain_type),
                updated_at=datetime.fromisoformat(updated_at),
                parent_id=UUID(parent_id) if parent_id else None,
                state=WorkflowState.model_validate_json(state_json),
            )
            workflows.append(workflow)

        return workflows

    @override
    def save(self, workflow: Workflow) -> Workflow:
        with sqlite3.connect(self.db_path) as conn:
            now = datetime.now(timezone.utc)
            workflow.updated_at = now
            current_snapshot_id = self._create_snapshot(conn, workflow.id, workflow.state, now)

            conn.execute(
                """
                UPDATE workflows
                SET current_snapshot_id = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    current_snapshot_id,
                    workflow.updated_at.isoformat(),
                    str(workflow.id),
                ),
            )
            conn.commit()

        return workflow

    @override
    def branch(self, snapshot_id: UUID) -> Workflow:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT
                    ws.workflow_id AS parent_workflow_id,
                    ws.state_json,
                    w.name,
                    w.description,
                    w.max_steps,
                    w.ticket_json,
                    w.domain_type
                FROM workflow_snapshots ws
                JOIN workflows w
                    ON w.id = ws.workflow_id
                WHERE ws.id = ?
                LIMIT 1
                """,
                (str(snapshot_id),),
            )
            row = cursor.fetchone()

        if row is None:
            raise SnapshotNotFound(f"Cannot branch: snapshot with ID {snapshot_id} does not exist")

        (
            parent_workflow_id,
            state_json,
            name,
            description,
            max_steps,
            ticket_json,
            domain_type,
        ) = row

        new_workflow = Workflow(
            ticket=Ticket.model_validate_json(ticket_json),
            domain_type=DomainType(domain_type),
            name=name,
            description=description,
            max_steps=max_steps,
            parent_id=UUID(parent_workflow_id),
            # state_json round-trip ensures deep copy (no shared references)
            state=WorkflowState.model_validate_json(state_json),
        )

        return self.persist(new_workflow)

    @override
    def history(self, workflow_id: UUID) -> WorkflowHistory:
        def _label_for_state(state: WorkflowState) -> str:
            if state.phase == WorkflowPhase.COLLECTING:
                return "Clarification updated"
            if state.phase == WorkflowPhase.SOLVING:
                return "Solution generated"
            if state.phase == WorkflowPhase.DISCUSSION:
                return "Solution refined"
            if state.phase == WorkflowPhase.DONE:
                return "Workflow completed"
            return "State updated"

        items: list[WorkflowHistoryItem] = []

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT
                    parent_id,
                    current_snapshot_id AS snapshot_id
                FROM workflows
                WHERE id = ?
                """,
                (str(workflow_id),),
            )
            row = cursor.fetchone()

            if row is None:
                raise WorkflowNotFound(f"Cannot get history: workflow with ID {workflow_id} does not exist")

            (parent_id, snapshot_id) = row
            parent_workflow_id = UUID(parent_id) if parent_id else None
            current_snapshot_id = UUID(snapshot_id)

            cursor = conn.execute(
                """
                SELECT
                    ws.id,
                    ws.created_at,
                    ws.state_json
                FROM workflow_snapshots ws
                WHERE ws.workflow_id = ?
                ORDER BY ws.created_at ASC
                """,
                (str(workflow_id),),
            )
            rows = cursor.fetchall()

        for row in rows:
            snapshot_id, created_at, state_json = row
            state = WorkflowState.model_validate_json(state_json)

            item = WorkflowHistoryItem(
                snapshot_id=UUID(snapshot_id),
                created_at=datetime.fromisoformat(created_at),
                phase=state.phase,
                label=_label_for_state(state),
            )
            items.append(item)

        return WorkflowHistory(
            workflow_id=workflow_id,
            parent_workflow_id=parent_workflow_id,
            current_snapshot_id=current_snapshot_id,
            items=items,
        )
