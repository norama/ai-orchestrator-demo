from typing import override

from app.application.chat_service import ChatService
from app.domain.chat import ChatMessage, ChatReply, ChatRole
from app.domain.workflow import WorkflowContext


class ParrotChatService(ChatService):
    @override
    def reply(
        self,
        ctx: WorkflowContext,
        user_message: ChatMessage,
    ) -> ChatReply:
        """Echo the user's message back to them."""
        content = user_message.content
        requires_solution_update = "solution" in content.lower()
        return ChatReply(
            message=ChatMessage(role=ChatRole.AI, content=user_message.content),
            requires_solution_update=requires_solution_update,
        )
