from uuid import uuid4

import pytest

from app.application.commands import AnswerStepCommand
from app.application.registry import WorkflowDomain
from app.application.workflow_service import WorkflowService
from app.domain.event import EventDisplayType, SolutionGeneratedEventData, SolutionGeneratedReason, WorkflowEventType
from app.domain.ticket import Ticket, TicketSource
from app.domain.workflow import Workflow, WorkflowCreate
from tests.fakes.fake_domain import FakeAnswerParser, FakeSolutionService, FakeStepGenerator
from tests.fakes.fake_repo import FakeWorkflowRepository


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
