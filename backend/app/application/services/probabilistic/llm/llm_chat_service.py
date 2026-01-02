from typing import override

from app.application.chat_service import ChatService
from app.application.services.probabilistic.llm.client.llm_client import LLMClient
from app.application.services.probabilistic.llm.domain.llm import LLMChatReply
from app.application.services.probabilistic.llm.utils.llm_call import call_llm_json
from app.domain.chat import ChatMessage, ChatReply, ChatRole
from app.domain.workflow import WorkflowContext


class LLMChatService(ChatService):
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def _build_prompt(self, ctx: WorkflowContext, msg: ChatMessage) -> str:
        recent = "\n".join(f"{m.role}: {m.content}" for m in ctx.chat_history.messages[-6:])

        return f"""
            You are assisting the user AFTER a solution has already been proposed.
            Based on the current proposed solution, the recent conversation and the last user message,
            decide if it is necessary to update the proposed solution.

            IMPORTANT RULES:
            - Do NOT directly rewrite or output the updated solution text.
            - Do NOT ask new clarification questions.
            - Do NOT propose new workflow steps or restart the workflow.
            - Your job is ONLY to:
            - reply to the user, AND
            - decide whether the solution needs to be regenerated.

            Set requires_solution_update = true IF AND ONLY IF:
            - The user explicitly asks to change, add, remove, or rewrite part of the solution, OR
            - The user points out missing information, an error, or a contradiction, OR
            - The user requests that the solution be updated for future reference.

            Return ONLY valid JSON matching this schema:
            {{
                "message": string, your reply to the user following the rules above
                "requires_solution_update": true or false
            }}

            Proposed solution:
            {ctx.solution.content if ctx.solution else "(no solution)"}

            Recent conversation:
            {recent}

            User message:
            {msg.content}
        """.strip()

    @override
    def reply(self, ctx: WorkflowContext, user_message: ChatMessage) -> ChatReply:
        prompt = self._build_prompt(ctx, user_message)

        try:
            data = call_llm_json(self.llm, prompt)
            parsed = LLMChatReply.model_validate(data)
            return ChatReply(
                message=ChatMessage(
                    role=ChatRole.AI,
                    content=parsed.message,
                ),
                requires_solution_update=parsed.requires_solution_update,
            )
        except Exception as e:
            return ChatReply(
                message=ChatMessage(
                    role=ChatRole.AI,
                    content=f"Sorry, I couldn't process your message at this time: {e}.",
                ),
                requires_solution_update=False,
            )
