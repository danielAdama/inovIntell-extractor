import dotenv
dotenv.load_dotenv(dotenv.find_dotenv(), override=True)
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Union, Optional
import json
import os

class BaseAgent:
    def __init__(
        self,
        name: str,
        model: str, 
        temperature: float,
        schema: Union[BaseModel, None] = None,
        system_message: Union[str, None] = None,
        tools: Union[list, None] = None,
        **kwargs,
        ):
        self.name = name
        self.schema = schema
        self.tools = tools if tools is not None else []
        self.system_message = system_message
        self.llm = ChatOpenAI(model=model, temperature=temperature, api_key=os.environ.get("OPENAI_API_KEY"))
        self.extra_args = kwargs

    def create_prompt(self) -> ChatPromptTemplate:
        """Create and return the ChatPromptTemplate."""
        raise NotImplementedError("Subclasses should implement this method.")

    def get_agent(self):
        """Return the configured agent."""
        prompt = self.create_prompt()
        return prompt | self.llm
    
    def set(self, **kwargs):
        """Generic method to update any attribute."""
        for key, value in kwargs.items():
            setattr(self, key, value)
            self.extra_args[key] = value  # Also update extra_args