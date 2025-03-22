import dotenv
dotenv.load_dotenv(dotenv.find_dotenv(), override=True)
from .base_agent import BaseAgent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from typing import List, Union, Optional
import os

class Agent(BaseAgent):
    def __init__(
            self,
            name: str,
            system_message: str,
            tools = None,
            schema: BaseModel = None,
            model: str = os.environ.get("DEFUALT_MODEL"),
            temperature: float = 0, **kwargs,
        ):
        super().__init__(
            name=name,
            model=model,
            temperature=temperature,
            schema=schema,
            system_message=system_message,
            tools=tools,
            **kwargs,
        )

    def create_prompt(self) -> ChatPromptTemplate:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_message),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        prompt = prompt.partial(
            name=self.name,
            **self.extra_args  # Dynamically include additional arguments
        )
        return prompt

    def get_agent(self):
        prompt = self.create_prompt()
        if self.schema:
            return prompt | self.llm.with_structured_output(self.schema)
        elif self.tools:
            return create_react_agent(self.llm, tools=self.tools, messages_modifier=prompt)
        else:
            return prompt | self.llm