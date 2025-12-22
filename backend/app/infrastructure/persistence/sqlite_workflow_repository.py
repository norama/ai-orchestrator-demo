import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import override
from uuid import uuid4

from app.domain.workflow import WorkflowState, WorkflowStateCreate
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
                    phase TEXT NOT NULL,
                    state_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    @override
    def persist(self, workflow: WorkflowState) -> WorkflowState:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO workflows (id, phase, state_json, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    workflow.id,
                    workflow.phase.value,
                    workflow.model_dump_json(),
                    workflow.updated_at.isoformat(),
                ),
            )
            conn.commit()

        return workflow

    @override
    def create(self, workflow_create: WorkflowStateCreate) -> WorkflowState:
        workflow_id = str(uuid4())
        workflow = WorkflowState(id=workflow_id, **workflow_create.model_dump())

        return self.persist(workflow)

    @override
    def get(self, workflow_id: str) -> WorkflowState | None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT state_json FROM workflows WHERE id = ?
                """,
                (workflow_id,),
            )
            row = cursor.fetchone()

            if row is None:
                return None

            state_json = row[0]
            return WorkflowState.model_validate_json(state_json)

    @override
    def list(self) -> list[WorkflowState]:
        workflows = []

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT state_json FROM workflows
                """
            )
            rows = cursor.fetchall()

            for row in rows:
                state_json = row[0]
                workflow = WorkflowState.model_validate_json(state_json)
                workflows.append(workflow)

        return workflows

    @override
    def save(self, workflow: WorkflowState) -> WorkflowState:
        now = datetime.now(timezone.utc)

        workflow = workflow.model_copy(update={"updated_at": now})

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                UPDATE workflows
                SET phase = ?, state_json = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    workflow.phase.value,
                    workflow.model_dump_json(),
                    workflow.updated_at.isoformat(),
                    workflow.id,
                ),
            )
            conn.commit()

        return workflow
