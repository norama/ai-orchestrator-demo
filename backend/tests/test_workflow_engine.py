from uuid import uuid4

import pytest

from app.application.commands import AddChatMessageCommand, AnswerStepCommand
from app.application.exceptions import InvalidWorkflowOperation
from app.application.registry import WorkflowDomain
from app.application.services.deterministic.protocols.parrot.parrot_chat_service import ParrotChatService
from app.application.solution_service import SolutionService
from app.application.step_generator import StepGenerator
from app.application.workflow_service import WorkflowService
from app.domain.chat import ChatRole
from app.domain.event import (
    ChatRepliedEventData,
    ClarificationUpdatedEventData,
    EventDisplayType,
    SolutionGeneratedEventData,
    SolutionGeneratedReason,
    WorkflowEventType,
)
from app.domain.streaming import StreamSink
from app.domain.ticket import Ticket, TicketSource
from app.domain.workflow import (
    ClarificationStep,
    NextStepDecision,
    Solution,
    Workflow,
    WorkflowContext,
    WorkflowCreate,
    WorkflowPhase,
)
from tests.fakes.fake_domain import FakeAnswerParser, FakeSolutionService, FakeStepGenerator
from tests.fakes.fake_repo import FakeWorkflowRepository


class TwoStepGenerator(StepGenerator):
    def propose_next(self, ctx: WorkflowContext) -> NextStepDecision:
        if len(ctx.steps) == 0:
            return NextStepDecision(
                next_step=ClarificationStep(prompt="Q1"),
                workflow_confidence=0.2,
                reason="initial",
            )
        if len(ctx.steps) == 1:
            return NextStepDecision(
                next_step=ClarificationStep(prompt="Q2"),
                workflow_confidence=0.6,
                reason="need more info",
            )
        return NextStepDecision(
            next_step=None,
            workflow_confidence=1.0,
            reason="done",
        )


class StaticSolutionService(SolutionService):
    def generate_solution(self, ctx: WorkflowContext, stream: StreamSink | None = None) -> Solution:
        return Solution(content="Solved", confidence=0.9, rationale="static")


@pytest.fixture
def fake_workflow_domain() -> WorkflowDomain:
    return WorkflowDomain(
        step_generator=FakeStepGenerator(),
        answer_parser=FakeAnswerParser(),
        solution_service=FakeSolutionService(),
    )


@pytest.fixture
def workflow_service(fake_workflow_domain: WorkflowDomain) -> WorkflowService:
    return WorkflowService(
        repo=FakeWorkflowRepository(),
        domain=fake_workflow_domain,
    )


@pytest.fixture
def multi_step_workflow_service() -> WorkflowService:
    domain = WorkflowDomain(
        step_generator=TwoStepGenerator(),
        answer_parser=FakeAnswerParser(),
        solution_service=StaticSolutionService(),
    )
    return WorkflowService(repo=FakeWorkflowRepository(), domain=domain)


@pytest.fixture
def chat_workflow_service() -> WorkflowService:
    domain = WorkflowDomain(
        step_generator=FakeStepGenerator(),
        answer_parser=FakeAnswerParser(),
        solution_service=FakeSolutionService(),
        chat_service=ParrotChatService(),
    )
    return WorkflowService(repo=FakeWorkflowRepository(), domain=domain)


@pytest.fixture
def workflow(workflow_service: WorkflowService) -> Workflow:
    return workflow_service.create(
        WorkflowCreate(
            ticket=Ticket(id=uuid4(), title="test", description="x", source=TicketSource.RESTFUL_API_DEV),
        )
    )


def test_workflow_creates_first_step(workflow: Workflow):
    state = workflow.state
    assert state.phase == "COLLECTING"
    assert len(state.steps) == 1
    assert state.solution is None


def test_workflow_waits_for_answer(workflow_service: WorkflowService, workflow: Workflow):
    workflow2 = workflow_service._process_until_waiting_or_done(workflow)  # type: ignore
    state = workflow2.state

    assert len(state.steps) == 1
    assert state.solution is None


def test_answer_triggers_solution(workflow_service: WorkflowService, workflow: Workflow):
    step = workflow.state.steps[0]

    workflow = workflow_service.answer_step(
        workflow.id,
        AnswerStepCommand(step_id=step.id, answer="anything"),
    )

    state = workflow.state
    assert state.solution is not None
    assert state.solution.content == "Solved"


def test_answer_emits_solution_generated_event(workflow_service: WorkflowService, workflow: Workflow):
    step = workflow.state.steps[0]

    workflow_service.answer_step(
        workflow.id,
        AnswerStepCommand(step_id=step.id, answer="anything"),
    )

    events = workflow_service.repo._events[workflow.id]  # type: ignore
    assert any(e.type == WorkflowEventType.SOLUTION_GENERATED for e in events)  # type: ignore


def test_branch_emits_workflow_branched_event(workflow_service: WorkflowService, workflow: Workflow):
    snapshot_id = uuid4()

    branched = workflow_service.branch(workflow.id, snapshot_id)

    assert branched.id != workflow.id
    assert branched.parent_id == workflow.id
    assert branched.parent_snapshot_id == snapshot_id

    events = workflow_service.repo._events[branched.id]  # type: ignore
    assert len(events) == 2  # type: ignore
    assert events[0].type == WorkflowEventType.WORKFLOW_BRANCHED  # type: ignore


def test_solution_generated_to_display():
    data = SolutionGeneratedEventData(
        reason=SolutionGeneratedReason.HIGH_CONFIDENCE,
        confidence=0.9,
        rationale="ok",
    )

    items = data.to_display()
    assert any(i.type == EventDisplayType.CONFIDENCE for i in items)
    assert any(i.type == EventDisplayType.TEXT and i.label == "Rationale" for i in items)


def test_create_emits_created_then_clarification_event(workflow_service: WorkflowService):
    created = workflow_service.create(
        WorkflowCreate(
            ticket=Ticket(id=uuid4(), title="phase0", description="x", source=TicketSource.RESTFUL_API_DEV),
        )
    )

    events = workflow_service.repo._events[created.id]  # type: ignore
    assert len(events) >= 2  # type: ignore
    assert events[0].type == WorkflowEventType.WORKFLOW_CREATED  # type: ignore
    assert events[1].type == WorkflowEventType.CLARIFICATION_UPDATED  # type: ignore

    data = ClarificationUpdatedEventData.model_validate(events[1].data)  # type: ignore
    assert data.prompt == "Q1"
    assert data.workflow_confidence == 0.1


def test_answer_step_emits_clarification_updated_when_next_step_exists(
    multi_step_workflow_service: WorkflowService,
):
    wf = multi_step_workflow_service.create(
        WorkflowCreate(
            ticket=Ticket(id=uuid4(), title="two-step", description="x", source=TicketSource.RESTFUL_API_DEV),
        )
    )

    step = wf.state.steps[0]
    wf = multi_step_workflow_service.answer_step(
        wf.id,
        AnswerStepCommand(step_id=step.id, answer="first answer"),
    )

    assert wf.state.phase == WorkflowPhase.COLLECTING
    assert len(wf.state.steps) == 2
    assert wf.state.steps[1].prompt == "Q2"

    events = multi_step_workflow_service.repo._events[wf.id]  # type: ignore
    assert events[-1].type == WorkflowEventType.CLARIFICATION_UPDATED  # type: ignore
    data = ClarificationUpdatedEventData.model_validate(events[-1].data)  # type: ignore
    assert data.prompt == "Q2"
    assert data.reason == "need more info"


def test_skip_to_solution_emits_manual_trigger_reason(workflow_service: WorkflowService, workflow: Workflow):
    updated = workflow_service.skip_to_solution(workflow.id)

    assert updated.state.solution is not None

    events = workflow_service.repo._events[workflow.id]  # type: ignore
    assert events[-1].type == WorkflowEventType.SOLUTION_GENERATED  # type: ignore

    data = SolutionGeneratedEventData.model_validate(events[-1].data)  # type: ignore
    assert data.reason == SolutionGeneratedReason.MANUAL_TRIGGER


def test_add_chat_message_emits_chat_replied_and_solution_updated(chat_workflow_service: WorkflowService):
    wf = chat_workflow_service.create(
        WorkflowCreate(
            ticket=Ticket(id=uuid4(), title="chat", description="x", source=TicketSource.RESTFUL_API_DEV),
            max_steps=0,
        )
    )

    assert wf.state.phase == WorkflowPhase.DISCUSSION

    wf = chat_workflow_service.add_chat_message(
        wf.id,
        AddChatMessageCommand(role=ChatRole.USER, content="Please update the solution"),
    )

    events = chat_workflow_service.repo._events[wf.id]  # type: ignore
    assert len(events) >= 2  # type: ignore
    assert events[-2].type == WorkflowEventType.CHAT_REPLIED  # type: ignore
    assert events[-1].type == WorkflowEventType.SOLUTION_UPDATED  # type: ignore

    chat_data = ChatRepliedEventData.model_validate(events[-2].data)  # type: ignore
    assert chat_data.message_role == ChatRole.USER
    assert chat_data.reply_role == ChatRole.AI
    assert chat_data.requires_solution_update is True


def test_add_chat_message_rejects_empty_message(chat_workflow_service: WorkflowService):
    workflow = chat_workflow_service.create(
        WorkflowCreate(
            ticket=Ticket(id=uuid4(), title="chat-empty", description="x", source=TicketSource.RESTFUL_API_DEV),
            max_steps=0,
        )
    )

    assert workflow.state.phase == WorkflowPhase.DISCUSSION

    with pytest.raises(InvalidWorkflowOperation, match="cannot be empty"):
        chat_workflow_service.add_chat_message(
            workflow.id,
            AddChatMessageCommand(role=ChatRole.USER, content="   "),
        )


def test_add_chat_message_rejects_non_discussion_phase(workflow_service: WorkflowService, workflow: Workflow):
    with pytest.raises(InvalidWorkflowOperation, match="DISCUSSION"):
        workflow_service.add_chat_message(
            workflow.id,
            AddChatMessageCommand(role=ChatRole.USER, content="hello"),
        )
