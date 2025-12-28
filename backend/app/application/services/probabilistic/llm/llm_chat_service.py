from typing import override

from app.application.chat_service import ChatService
from app.application.services.probabilistic.llm.client.llm_client import LLMClient
from app.domain.chat import ChatMessage, ChatRole
from app.domain.workflow import WorkflowContext


class LLMChatService(ChatService):
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def _build_prompt(self, ctx: WorkflowContext, msg: ChatMessage) -> str:
        recent = "\n".join(f"{m.role}: {m.content}" for m in ctx.chat_history.messages[-6:])

        return f"""
            You are assisting the user AFTER a solution has already been proposed.

            IMPORTANT RULES:
            - Do NOT change the solution.
            - Do NOT ask new clarification questions.
            - Do NOT propose new steps.
            - Do NOT suggest restarting the workflow.
            - You may explain, elaborate, clarify, or give usage advice only.

            Proposed solution:
            {ctx.solution.content if ctx.solution else "(no solution)"}

            Recent conversation:
            {recent}

            User message:
            {msg.content}
        """.strip()

    @override
    def reply(self, ctx: WorkflowContext, user_message: ChatMessage) -> ChatMessage:
        prompt = self._build_prompt(ctx, user_message)

        try:
            content = self.llm.complete(prompt)
        except Exception:
            content = "I'm unable to respond right now."

        return ChatMessage(
            role=ChatRole.AI,
            content=content,
        )
