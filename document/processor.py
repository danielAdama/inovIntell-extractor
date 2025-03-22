from agents.agent import Agent
from langchain_core.messages import HumanMessage
from utils.app_utils import AppUtil
import json
from typing import Dict, List, Optional, Tuple, Union
from config.config_helper import Configuration
from config.logger import Logger

logger = Logger(__name__)
prompt_settings = Configuration().get_config('prompt')['agent_templates']

class Preprocess:
    def __init__(self):
        self.initialize_agents()

    def initialize_agents(self):
        self.demographics_extractor_agent = self.create_agent(
            Agent, "Expert Processor of Real-World Evidence (RWE) Studies in Oncology", prompt_settings['demographics_extraction_prompt']
        )
        self.results_extractor_agent = self.create_agent(
            Agent, "Expert Processor of Real-World Evidence (RWE) Studies in Oncology", prompt_settings['results_extraction_prompt']
        )
        self.demographics_extractor_agent_active = None
        self.results_extractor_agent_active = None
    
    def create_agent(self, agent_class, name, system_message, temperature=0, schema=None, **kwargs):
        return agent_class(
            name=name,
            schema=schema,
            system_message=system_message,
            temperature=temperature,
            **kwargs,
        )
    
    def get_demographics(self, file_content, extractor_json_schema) -> Dict:
        self.demographics_extractor_agent.set(
            content=file_content,
            extractor_json_schema=AppUtil.load_json(f"{extractor_json_schema}_schema.json")
        )
        self.demographics_extractor_agent_active = self.demographics_extractor_agent.get_agent()

        output = self.demographics_extractor_agent_active.invoke(
            {"messages":[
                HumanMessage(
                    content=[
                        {"type": "text", "text": "What is the demographics extractions on Real-World Evidence in oncology?"}
                    ]
                )
            ]}
        )
        extracted_data = json.loads(AppUtil.remove_code_blocks(output.content))
        return extracted_data
    
    def get_result(self, file_content, demographics, extractor_json_schema) -> Dict:
        self.results_extractor_agent.set(
            content=file_content,
            demographics=demographics,
            extractor_json_schema=AppUtil.load_json(f"{extractor_json_schema}_schema.json")
        )
        self.results_extractor_agent_active = self.results_extractor_agent.get_agent()

        output = self.results_extractor_agent_active.invoke(
            {"messages":[
                HumanMessage(
                    content=[
                        {"type": "text", "text": "What is the results extractions on Real-World Evidence in oncology?"}
                    ]
                )
            ]}
        )
        extracted_data = json.loads(AppUtil.remove_code_blocks(output.content))
        return extracted_data