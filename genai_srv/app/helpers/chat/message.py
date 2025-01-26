from langchain_core.messages.ai import AIMessage
from langchain_core.messages import AnyMessage
from langchain_core.messages.human import HumanMessage


def state_conversation_messages(messages: list[AnyMessage]):
    result = []

    for i, message in enumerate(messages, 1):
        if message.type == "human":
            result.append(HumanMessage(content=message.content))
        else:
            result.append(AIMessage(content=message.content))

    return result
