from typing_extensions import Protocol

from app.domain.chat import ChatMessage, ChatReply
from app.domain.workflow import WorkflowContext


class ChatService(Protocol):
    def reply(
        self,
        ctx: WorkflowContext,
        user_message: ChatMessage,
    ) -> ChatReply:
        """Generate a reply to the user's message within the given workflow context."""
        ...
