from uuid import uuid4

from app.application.commands import AnswerStepCommand
from app.application.services.deterministic.printer.printer_answer_parser import PrinterAnswerParser
from app.application.services.deterministic.printer.printer_solution_service import PrinterSolutionService
from app.application.services.deterministic.printer.printer_step_generator import PrinterStepGenerator
from app.application.workflow_service import WorkflowService
from app.domain.config import DomainType
from app.domain.ticket import Ticket, TicketSource
from app.domain.workflow import WorkflowStateCreate
from tests.fakes.fake_repo import FakeWorkflowRepository


def test_printer_happy_path():
    repo = FakeWorkflowRepository()

    service = WorkflowService(
        repo=repo,
        step_generator=PrinterStepGenerator(),
        answer_parser=PrinterAnswerParser(),
        solution_service=PrinterSolutionService(),
    )

    workflow = service.create(
        WorkflowStateCreate(
            ticket=Ticket(id=uuid4(), title="test", description="x", source=TicketSource.RESTFUL_API_DEV),
            domain=DomainType.PRINTER,
        )
    )

    # Step 1
    step1 = workflow.steps[0]
    workflow = service.answer_step(
        workflow.id,
        AnswerStepCommand(step_id=step1.id, answer="yes"),
    )

    # Step 2
    step2 = workflow.steps[1]
    workflow = service.answer_step(
        workflow.id,
        AnswerStepCommand(step_id=step2.id, answer="Nothing happens"),
    )

    assert workflow.solution is not None
    assert workflow.solution.confidence >= 0.8
