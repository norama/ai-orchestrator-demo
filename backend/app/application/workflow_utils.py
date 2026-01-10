from app.domain.chat import ChatRole
from app.domain.workflow import WaitingReason, WorkflowPhase, WorkflowState


def _has_open_step(state: WorkflowState) -> bool:
    return any(step.answer is None for step in state.steps)


def _is_waiting_for_chat_input(state: WorkflowState) -> bool:
    if not state.chat_history.messages:
        return True
    last_msg = state.chat_history.messages[-1]
    return last_msg.role != ChatRole.USER


def get_waiting_reason(state: WorkflowState) -> WaitingReason | None:
    if state.phase == WorkflowPhase.COLLECTING and state.skipped:
        return None
    if state.phase == WorkflowPhase.COLLECTING and _has_open_step(state):
        return WaitingReason.ANSWER_NEEDED
    if state.phase == WorkflowPhase.DISCUSSION and _is_waiting_for_chat_input(state):
        return WaitingReason.CHAT
    return None


def get_workflow_confidence(state: WorkflowState) -> float | None:
    if state.last_decision:
        return state.last_decision.workflow_confidence
    return None


def is_waiting_for_user(state: WorkflowState) -> bool:
    return get_waiting_reason(state) is not None
