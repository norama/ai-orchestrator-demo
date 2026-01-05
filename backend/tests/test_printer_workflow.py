from uuid import uuid4

import pytest

from app.application.commands import AnswerStepCommand
from app.application.registry import WorkflowDomain
from app.application.services.deterministic.protocols.printer.printer_answer_parser import PrinterAnswerParser
from app.application.services.deterministic.protocols.printer.printer_solution_service import PrinterSolutionService
from app.application.services.deterministic.protocols.printer.printer_step_generator import PrinterStepGenerator
from app.application.workflow_service import WorkflowService
from app.domain.config import DomainType
from app.domain.ticket import Ticket, TicketSource
from app.domain.workflow import Workflow, WorkflowCreate
from tests.fakes.fake_repo import FakeWorkflowRepository


@pytest.fixture
def printer_workflow_domain() -> WorkflowDomain:
    return WorkflowDomain(
        step_generator=PrinterStepGenerator(),
        answer_parser=PrinterAnswerParser(),
        solution_service=PrinterSolutionService(),
    )


@pytest.fixture
def workflow_service(printer_workflow_domain: WorkflowDomain) -> WorkflowService:
    return WorkflowService(
        repo=FakeWorkflowRepository(),
        domain=printer_workflow_domain,
    )


@pytest.fixture
def workflow(workflow_service: WorkflowService) -> Workflow:
    return workflow_service.create(
        WorkflowCreate(
            ticket=Ticket(id=uuid4(), title="test", description="x", source=TicketSource.RESTFUL_API_DEV),
            domain_type=DomainType.PRINTER,
        )
    )


def test_printer_happy_path(workflow_service: WorkflowService, workflow: Workflow):
    # Step 1
    step1 = workflow.state.steps[0]
    workflow = workflow_service.answer_step(
        workflow.id,
        AnswerStepCommand(step_id=step1.id, answer="yes"),
    )

    # Step 2
    step2 = workflow.state.steps[1]
    workflow = workflow_service.answer_step(
        workflow.id,
        AnswerStepCommand(step_id=step2.id, answer="Nothing happens"),
    )

    assert workflow.state.solution is not None
    assert workflow.state.solution.confidence >= 0.8
