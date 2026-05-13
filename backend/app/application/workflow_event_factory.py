from uuid import UUID

from app.application.exceptions import InvalidWorkflowOperation
from app.domain.chat import ChatMessage
from app.domain.event import (
    ChatRepliedEventData,
    ClarificationUpdatedEventData,
    SolutionGeneratedEventData,
    SolutionGeneratedReason,
    WorkflowBranchedEventData,
    WorkflowCreatedEventData,
    WorkflowEventCreate,
    WorkflowEventType,
)
from app.domain.workflow import Workflow, WorkflowCreate


class WorkflowEventFactory:
    @staticmethod
    def workflow_created(workflow_create: WorkflowCreate) -> WorkflowEventCreate:
        return WorkflowEventCreate(
            type=WorkflowEventType.WORKFLOW_CREATED,
            data=WorkflowCreatedEventData(
                ticket_title=workflow_create.ticket.title,
                domain_type=workflow_create.domain_type,
                name=workflow_create.name,
            ).model_dump(),
        )

    @staticmethod
    def workflow_branched(parent_workflow: Workflow, snapshot_id: UUID) -> WorkflowEventCreate:
        return WorkflowEventCreate(
            type=WorkflowEventType.WORKFLOW_BRANCHED,
            data=WorkflowBranchedEventData(
                ticket_title=parent_workflow.ticket.title,
                domain_type=parent_workflow.domain_type,
                parent_name=parent_workflow.name,
                name=parent_workflow.name,
                parent_workflow_id=parent_workflow.id,
                parent_snapshot_id=snapshot_id,
            ).model_dump(),
        )

    @staticmethod
    def clarification_updated(workflow: Workflow) -> WorkflowEventCreate:
        if workflow.state.last_decision is None or workflow.state.last_decision.next_step is None:
            raise InvalidWorkflowOperation("Cannot emit clarification update without a next step decision")
        return WorkflowEventCreate(
            type=WorkflowEventType.CLARIFICATION_UPDATED,
            data=ClarificationUpdatedEventData(
                prompt=workflow.state.last_decision.next_step.prompt,
                workflow_confidence=workflow.state.last_decision.workflow_confidence,
                reason=workflow.state.last_decision.reason,
            ).model_dump(),
        )

    @staticmethod
    def solution_generated(
        workflow: Workflow,
        reason: SolutionGeneratedReason | None = None,
    ) -> WorkflowEventCreate:
        if workflow.state.solution is None:
            raise InvalidWorkflowOperation("Cannot emit solution generated event without a solution")
        generated_reason = reason or (
            SolutionGeneratedReason.HIGH_CONFIDENCE
            if len(workflow.state.steps) < workflow.max_steps
            else SolutionGeneratedReason.MAX_STEPS_REACHED
        )
        return WorkflowEventCreate(
            type=WorkflowEventType.SOLUTION_GENERATED,
            data=SolutionGeneratedEventData(
                reason=generated_reason,
                confidence=workflow.state.solution.confidence,
                rationale=workflow.state.solution.rationale,
            ).model_dump(),
        )

    @staticmethod
    def chat_replied(
        user_message: ChatMessage,
        reply_message: ChatMessage,
        requires_solution_update: bool,
    ) -> WorkflowEventCreate:
        return WorkflowEventCreate(
            type=WorkflowEventType.CHAT_REPLIED,
            data=ChatRepliedEventData(
                message_role=user_message.role,
                message_content=user_message.content,
                reply_role=reply_message.role,
                reply_content=reply_message.content,
                requires_solution_update=requires_solution_update,
            ).model_dump(),
        )

    @staticmethod
    def solution_updated() -> WorkflowEventCreate:
        return WorkflowEventCreate(type=WorkflowEventType.SOLUTION_UPDATED)
