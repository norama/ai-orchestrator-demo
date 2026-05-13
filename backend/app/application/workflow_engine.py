from app.application.registry import WorkflowDomain
from app.application.workflow_utils import is_waiting_for_user
from app.domain.chat import ChatRole
from app.domain.streaming import StreamSink
from app.domain.workflow import ChatMutationResult, Workflow, WorkflowContext, WorkflowPhase


class WorkflowEngine:
    """
    Phase-by-phase state machine for workflow execution.

    COLLECTING  – steps allowed; chat_history ignored
    SOLVING     – no new steps; solution generated
    DISCUSSION  – chat_history active; no new steps; solution immutable (for now)
    DONE        – immutable terminal state; set when no chat service is configured
    """

    def __init__(self, domain: WorkflowDomain):
        self.domain = domain

    @staticmethod
    def _build_context(workflow: Workflow) -> WorkflowContext:
        return WorkflowContext(
            workflow_id=workflow.id,
            domain_type=workflow.domain_type,
            ticket=workflow.ticket,
            steps=workflow.state.steps,
            last_decision=workflow.state.last_decision,
            solution=workflow.state.solution,
            chat_history=workflow.state.chat_history,
            skipped=workflow.state.skipped,
            max_steps=workflow.max_steps,
            phase=workflow.state.phase,
        )

    def _process_collecting_phase(self, workflow: Workflow) -> Workflow:
        state = workflow.state

        if state.skipped or len(state.steps) >= workflow.max_steps:
            state.phase = WorkflowPhase.SOLVING
            return workflow

        decision = self.domain.step_generator.propose_next(self._build_context(workflow))

        state.last_decision = decision
        if decision.next_step:
            state.steps.append(decision.next_step)
            return workflow

        state.phase = WorkflowPhase.SOLVING
        return workflow

    def _process_solving_phase(self, workflow: Workflow, stream: StreamSink | None = None) -> Workflow:
        workflow.state.solution = self.domain.solution_service.generate_solution(self._build_context(workflow), stream)
        workflow.state.phase = WorkflowPhase.DISCUSSION if self.domain.chat_service else WorkflowPhase.DONE
        return workflow

    def _process_discussion_phase(self, workflow: Workflow) -> Workflow:
        state = workflow.state
        discussion_result = ChatMutationResult(solution_updated=False)

        if self.domain.chat_service and state.chat_history.messages:
            last_msg = state.chat_history.messages[-1]
            if last_msg.role == ChatRole.USER:
                reply = self.domain.chat_service.reply(self._build_context(workflow), last_msg)
                state.chat_history.add_message(reply.message)
                if reply.requires_solution_update:
                    state.solution = self.domain.solution_service.generate_solution(self._build_context(workflow))
                    discussion_result = ChatMutationResult(solution_updated=True)

        state.discussion_result = discussion_result
        return workflow

    def process_once(self, workflow: Workflow, stream: StreamSink | None = None) -> Workflow:
        state = workflow.state
        state.last_decision = None
        state.discussion_result = None

        match state.phase:
            case WorkflowPhase.DONE:
                return workflow
            case WorkflowPhase.COLLECTING:
                return self._process_collecting_phase(workflow)
            case WorkflowPhase.SOLVING:
                return self._process_solving_phase(workflow, stream)
            case WorkflowPhase.DISCUSSION:
                return self._process_discussion_phase(workflow)

        raise ValueError(f"Unsupported workflow phase: {state.phase}")

    def run_until_waiting_or_done(self, workflow: Workflow, stream: StreamSink | None = None) -> Workflow:
        while not is_waiting_for_user(workflow.state) and workflow.state.phase != WorkflowPhase.DONE:
            workflow = self.process_once(workflow, stream)
        return workflow
