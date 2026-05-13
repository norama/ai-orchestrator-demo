from uuid import UUID

from app.application.commands import (
    AddChatMessageCommand,
    AnswerStepCommand,
)
from app.application.exceptions import InvalidWorkflowOperation, WorkflowNotFound
from app.application.registry import WorkflowDomain
from app.application.workflow_engine import WorkflowEngine
from app.application.workflow_event_factory import WorkflowEventFactory
from app.domain.chat import ChatMessage
from app.domain.event import (
    SolutionGeneratedReason,
    WorkflowEventCreate,
)
from app.domain.streaming import StreamSink
from app.domain.workflow import (
    Workflow,
    WorkflowCreate,
    WorkflowPhase,
)
from app.infrastructure.persistence.workflow_repository import WorkflowRepository


class WorkflowService:
    def __init__(self, repo: WorkflowRepository, domain: WorkflowDomain):
        self.repo = repo
        self.domain = domain
        self.engine = WorkflowEngine(domain)
        self.event_factory = WorkflowEventFactory()

    def _process_until_waiting_or_done(self, workflow: Workflow, stream: StreamSink | None = None) -> Workflow:
        return self.engine.run_until_waiting_or_done(workflow, stream)

    @staticmethod
    def _ensure_phase(workflow: Workflow, phase: WorkflowPhase, message: str) -> None:
        if workflow.state.phase != phase:
            raise InvalidWorkflowOperation(message)

    @staticmethod
    def _next_unanswered_step(workflow: Workflow, step_id: UUID):
        step = next((s for s in workflow.state.steps if s.id == step_id), None)
        if step is None:
            raise InvalidWorkflowOperation("Step not found")
        if step.answer is not None:
            raise InvalidWorkflowOperation("Step already answered")
        return step

    def _events_after_engine_run(self, workflow: Workflow) -> list[WorkflowEventCreate]:
        events: list[WorkflowEventCreate] = []
        if workflow.state.phase == WorkflowPhase.COLLECTING:
            events.append(self.event_factory.clarification_updated(workflow))
        if workflow.state.phase in (WorkflowPhase.DISCUSSION, WorkflowPhase.DONE):
            events.append(self.event_factory.solution_generated(workflow))
        return events

    # ------- Commands with processing --------

    def answer_step(self, workflow_id: UUID, cmd: AnswerStepCommand, stream: StreamSink | None = None) -> Workflow:
        workflow = self.get_workflow(workflow_id)
        self._ensure_phase(workflow, WorkflowPhase.COLLECTING, "Answers can only be added in COLLECTING phase")

        step = self._next_unanswered_step(workflow, cmd.step_id)

        step.answer = cmd.answer

        # domain-specific interpretation hook
        if self.domain.answer_parser:
            self.domain.answer_parser.parse_answer(step)

        workflow = self._process_until_waiting_or_done(workflow, stream)
        return self.repo.update_workflow(workflow, self._events_after_engine_run(workflow))

    def skip_to_solution(self, workflow_id: UUID, stream: StreamSink | None = None) -> Workflow:
        workflow = self.get_workflow(workflow_id)
        self._ensure_phase(workflow, WorkflowPhase.COLLECTING, "Can only skip to solution in COLLECTING phase")

        workflow.state.skipped = True

        workflow = self._process_until_waiting_or_done(workflow, stream)

        event = self.event_factory.solution_generated(
            workflow,
            reason=SolutionGeneratedReason.MANUAL_TRIGGER,
        )

        return self.repo.update_workflow(workflow, [event])

    # ------- Creation --------

    def create(self, workflow_create: WorkflowCreate) -> Workflow:
        workflow = Workflow(**workflow_create.model_dump())
        event = self.event_factory.workflow_created(workflow_create)
        return self.start(workflow, initial_events=[event])

    def branch(self, workflow_id: UUID, snapshot_id: UUID) -> Workflow:
        parent_workflow = self.get_workflow(workflow_id)
        state = self.repo.get_snapshot(workflow_id, snapshot_id)

        workflow = Workflow(
            ticket=parent_workflow.ticket,
            domain_type=parent_workflow.domain_type,
            name=parent_workflow.name,
            description=parent_workflow.description,
            max_steps=parent_workflow.max_steps,
            parent_id=parent_workflow.id,
            parent_snapshot_id=snapshot_id,
            state=state,
        )

        event = self.event_factory.workflow_branched(parent_workflow, snapshot_id)
        return self.start(workflow, initial_events=[event])

    def start(
        self,
        workflow: Workflow,
        *,
        initial_events: list[WorkflowEventCreate] | None = None,
    ) -> Workflow:
        workflow = self._process_until_waiting_or_done(workflow)

        events: list[WorkflowEventCreate] = []
        if initial_events:
            events.extend(initial_events)

        if workflow.state.phase == WorkflowPhase.COLLECTING:
            events.append(self.event_factory.clarification_updated(workflow))
        else:
            events.append(self.event_factory.solution_generated(workflow))

        return self.repo.insert_workflow(workflow, events)

    # -------- Queries --------

    def get_workflow(self, workflow_id: UUID) -> Workflow:
        workflow = self.repo.get_workflow(workflow_id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow {workflow_id} not found")
        return workflow

    def list_workflows(self) -> list[Workflow]:
        return self.repo.get_workflows()

    def add_chat_message(
        self,
        workflow_id: UUID,
        cmd: AddChatMessageCommand,
    ) -> Workflow:
        workflow = self.get_workflow(workflow_id)
        self._ensure_phase(workflow, WorkflowPhase.DISCUSSION, "Chat is only available in DISCUSSION phase")

        if not cmd.content.strip():
            raise InvalidWorkflowOperation("Chat message content cannot be empty")

        user_message = ChatMessage(
            role=cmd.role,
            content=cmd.content,
        )

        workflow.state.chat_history.add_message(user_message)

        workflow = self._process_until_waiting_or_done(workflow)

        events: list[WorkflowEventCreate] = []
        requires_solution_update = (
            workflow.state.discussion_result.solution_updated if workflow.state.discussion_result else False
        )
        events.append(
            self.event_factory.chat_replied(
                user_message,
                workflow.state.chat_history.messages[-1],
                requires_solution_update,
            )
        )
        if requires_solution_update:
            events.append(self.event_factory.solution_updated())

        return self.repo.update_workflow(workflow, events)
