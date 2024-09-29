from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory

from app.web.api import get_messages_by_conversation_id, add_message_to_conversation


class SqlMessageHistory(BaseChatMessageHistory, BaseModel):
    conversation_id: str

    @property
    def messages(self):
        return get_messages_by_conversation_id(self.conversation_id)

    def add_message(self, message):
        """
        Add a new message to the SQLite database
        """
        return add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=message.content,
        )

    def clear(self):
        # TODO: Add logic for clear
        pass


def build_memory(chat_args):
    return ConversationBufferMemory(
        chat_memory=SqlMessageHistory(conversation_id=chat_args.conversation_id),
        return_messages=True,  # Return messages in an object rather than string
        memory_key="chat_history",
        output_key="answer",
    )
