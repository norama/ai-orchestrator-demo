from typing import override

from app.application.chat_service import ChatService
from app.domain.chat import ChatMessage, ChatRole
from app.domain.workflow import WorkflowContext


class ParrotChatService(ChatService):
    @override
    def reply(
        self,
        ctx: WorkflowContext,
        user_message: ChatMessage,
    ) -> ChatMessage:
        """Echo the user's message back to them."""
        return ChatMessage(role=ChatRole.AI, content=user_message.content)
