from uuid import uuid4

import pytest

from app.application.commands import AnswerStepCommand
from app.application.registry import WorkflowDomain
from app.application.workflow_service import WorkflowService
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
