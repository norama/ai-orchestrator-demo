from uuid import uuid4

import pytest

from app.application.commands import AnswerStepCommand
from app.application.workflow_service import WorkflowService
from app.domain.ticket import Ticket, TicketSource
from app.domain.workflow import WorkflowState, WorkflowStateCreate
from tests.fakes.fake_domain import FakeAnswerParser, FakeSolutionService, FakeStepGenerator
from tests.fakes.fake_repo import FakeWorkflowRepository


@pytest.fixture
def workflow_service() -> WorkflowService:
    return WorkflowService(
        repo=FakeWorkflowRepository(),
        step_generator=FakeStepGenerator(),
        answer_parser=FakeAnswerParser(),
        solution_service=FakeSolutionService(),
    )


@pytest.fixture
def workflow(workflow_service: WorkflowService) -> WorkflowState:
    return workflow_service.create(
        WorkflowStateCreate(
            ticket=Ticket(id=uuid4(), title="test", description="x", source=TicketSource.RESTFUL_API_DEV),
        )
    )


def test_workflow_creates_first_step(workflow: WorkflowState):
    assert workflow.phase == "COLLECTING"
    assert len(workflow.steps) == 1
    assert workflow.solution is None


def test_workflow_waits_for_answer(workflow_service: WorkflowService, workflow: WorkflowState):
    workflow2 = workflow_service._process_until_waiting(workflow)  # type: ignore

    assert len(workflow2.steps) == 1
    assert workflow2.solution is None


def test_answer_triggers_solution(workflow_service: WorkflowService, workflow: WorkflowState):
    step = workflow.steps[0]

    workflow = workflow_service.answer_step(
        workflow.id,
        AnswerStepCommand(step_id=step.id, answer="anything"),
    )

    assert workflow.solution is not None
    assert workflow.solution.content == "Solved"
