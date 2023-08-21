
from __future__ import annotations

from typing import Dict, List, Sequence
from langchain.chat_models.base import BaseChatModel
from langchain.chat_models import ChatOpenAI
import json
import yaml
from langchain.callbacks import get_openai_callback

import logging
from langchain.schema import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    BaseMessage,
    FunctionMessage,
    ChatMessage
)
from termcolor import colored


class LanguageFunction:
    """
    Single turn natural language function which expects a text query in a structured format and returns a text response.
    """
    def __init__(self, config: Dict, **model_kwargs) -> None:
        """
        Initialize the function
        Args:
            config (Dict): The containing the function's configuration.
        """
        function = dict(config["function"])
        model = dict(config["model"])
        model_kwargs.update(model)
        self.model_kwargs = model_kwargs
        self.system_message = SystemMessage(content = function.get("system_message", ""))
        self.few_shot_prompt = parse_conversation(function.get("few_shot_prompt", []))
        self.user_message_template: str = function["user_message_template"]

        self.reset_messages()

        self.chat_model: BaseChatModel = ChatOpenAI(**self.model_kwargs)

    def reset_messages(self) -> None:
        """
        Reset the agent's conversation.
        """
        self.messages: List[BaseMessage] = []
    
    def __call__(self, callback = False, **kwargs) -> Dict:
        """
        Call the Agent Function with the given arguments.

        Args:
            callback (bool): Whether to use the OpenAI callback for logging
            kwargs (Dict): The arguments to the function.
        """
        message = HumanMessage(content = self.user_message_template.format(**kwargs))
        self.messages.append(message)
        return self._call_model(callback)
    
    def _call_model(self, callback_on: bool) -> Dict:
        if callback_on:
            with get_openai_callback() as callback:
                response = self.chat_model([self.system_message, *self.few_shot_prompt, *self.messages])
        else:
            response = self.chat_model([self.system_message, *self.few_shot_prompt, *self.messages])
        self.messages.append(response)
        chat_string = get_buffer_string(self.messages)
        logging.debug(f'Language Function thread:\n{chat_string}')
        if callback_on:
            logging.debug(f'Total prompt tokens: {callback.prompt_tokens}')
            logging.debug(f'Total completion tokens: {callback.completion_tokens}')
            logging.debug(f'Total Cost: ${callback.total_cost:.7f}')
        self.reset_messages()
        try:
            response_dict = json.loads(response.content)
        except json.decoder.JSONDecodeError:
            response_dict = {"response": response.content}
        return response_dict

    @classmethod
    def from_yaml(cls, filepath: str) -> LanguageFunction:
        """
        Load an agent from a YAML file.

        Args:
            filepath (str): The path to the YAML file.

        Returns:
            Agent: The agent.
        """
        yaml_obj = load_yaml_file(filepath)
        return cls(yaml_obj)

def load_yaml_file(filepath: str) -> List[Dict]:
    """
    Load a YAML file and return its contents as a dictionary.

    Args:
        filepath (str): The path to the YAML file.

    Returns:
        Dict: The contents of the YAML file as a dictionary.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        yaml_obj = yaml.safe_load(file)
    return yaml_obj

def parse_conversation(raw_messages: List[Dict]) -> List[BaseMessage]:
    """
    Parse a chat thread JSON object into a list of Messages.
    """
    message_roles  = {
        "user": HumanMessage,
        "assistant": AIMessage,
        "system": SystemMessage,
    }

    messages = []
    for message in raw_messages:
        message_type = message_roles[message["role"]]
        messages.append(message_type(content=message["content"]))

    return messages

def get_buffer_string(
    messages: Sequence[BaseMessage], human_prefix: str = "Input", ai_prefix: str = "Output"
) -> str:
    """Convert sequence of Messages to strings and concatenate them into one string.

    Args:
        messages: Messages to be converted to strings.
        human_prefix: The prefix to prepend to contents of HumanMessages.
        ai_prefix: THe prefix to prepend to contents of AIMessages.

    Returns:
        A single string concatenation of all input messages.

    Example:
        .. code-block:: python

            from langchain.schema import AIMessage, HumanMessage

            messages = [
                HumanMessage(content="Hi, how are you?"),
                AIMessage(content="Good, how are you?"),
            ]
            get_buffer_string(messages)
            # -> "Human: Hi, how are you?\nAI: Good, how are you?"
    """
    role_to_color = {
        "System": "red",
        human_prefix: "green",
        ai_prefix: "blue",
        "Function": "magenta",
    }
    formatted_messages = []
    for m in messages:
        if isinstance(m, HumanMessage):
            role = human_prefix
        elif isinstance(m, AIMessage):
            role = ai_prefix
        elif isinstance(m, SystemMessage):
            role = "System"
        elif isinstance(m, FunctionMessage):
            role = "Function"
        elif isinstance(m, ChatMessage):
            role = m.role
        else:
            raise ValueError(f"Got unsupported message type: {m}")
        prefix_len = len(f'{role}: ')
        message_content = m.content
        message_lines = message_content.split("\n")
        if len(message_lines) > 1: # To align indent
            message_content = "\n".join(
                [message_lines[0]]
                + [" " * prefix_len + line for line in message_lines[1:]]
            )
        message = f"{role}: {message_content}"
        if isinstance(m, AIMessage) and "function_call" in m.additional_kwargs:
            message += f"{m.additional_kwargs['function_call']}"

        formatted_messages.append(colored(message, role_to_color[role]))
    return "\n".join(formatted_messages)


