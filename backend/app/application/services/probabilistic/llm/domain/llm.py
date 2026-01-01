from enum import Enum

from pydantic import BaseModel


class LLMAction(str, Enum):
    ASK = "ASK"
    DONE = "DONE"


class LLMNextStep(BaseModel):
    action: LLMAction
    prompt: str | None = None
    workflow_confidence: float
    reason: str

    @staticmethod
    def validate_semantics(obj: "LLMNextStep") -> "LLMNextStep":
        if obj.action == LLMAction.ASK and not obj.prompt:
            raise ValueError("prompt required when action='ask'")
        if obj.action == LLMAction.DONE and obj.prompt is not None:
            raise ValueError("prompt must be null when action='done'")
        if not (0.0 <= obj.workflow_confidence <= 1.0):
            raise ValueError("workflow_confidence out of range")
        return obj


class LLMSolution(BaseModel):
    content: str
    solution_confidence: float  # 0.0–1.0
    rationale: str | None = None

    @staticmethod
    def validate_semantics(obj: "LLMSolution") -> "LLMSolution":
        if not obj.content.strip():
            raise ValueError("content is required")
        if not (0.0 <= obj.solution_confidence <= 1.0):
            raise ValueError("solution_confidence out of range")
        return obj


class LLMChatReply(BaseModel):
    message: str
    requires_solution_update: bool
