from agents.agent import Agent
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from utils.app_utils import AppUtil
import json
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path


class Preprocess:
    def __init__(self):
        self.initialize_agents()

    def initialize_agents(self):
        self.extractor_agent = self.create_agent(
            Agent, "Expert Processor of Real-World Evidence (RWE) Studies in Oncology", self.extraction_system_message
        )
        self.extractor_agent_active = None
    
    def create_agent(self, agent_class, name, system_message, temperature=0, schema=None, **kwargs):
        return agent_class(
            name=name,
            schema=schema,
            system_message=system_message,
            temperature=temperature,
            **kwargs,
        )
    
    @property
    def extraction_system_message(self):
        return """You are an {name} tasked with extracting information from a content based on a dynamic extractor json schema form. 
    The schema specifies keys and their descriptions, and the content contains the corresponding values provided from a document. Your goal is to:
    1. Parse the given content to extract human-provided values corresponding to each key in the form.
    2. Ensure the extracted values are matched with the correct keys as specified in the form.
    3. Dynamically adapt to any structure of the form to extract the required information accurately.
    4. Output a JSON object with the keys from the form and the corresponding extracted values from the document, but NO Explanation along with the output

    ### Input Example:

    #### Content:
    <content>{content}</content>

    #### Form:
    <extractor_json_schema>{extractor_json_schema}</extractor_json_schema>

    ### Expected Output:
    The output should be a JSON object containing the keys from the form and the corresponding values from the document:

    a. **Adhere to the Schema:**  
        The final JSON must include the following keys and structure:
        - **treatment_regimens:** Array of treatment regimens mentioned.
        - **countries:** Array of countries where the study was conducted.
        - **populations:** Array of objects with:
            - **stage_histology:** Combined disease stage and histology information.
            - **pdl1_status:** PD-L1 expression status.
            - **n:** Population size.
        - **results:** An object including:
            - **median_os:** Median overall survival.
            - **median_rw_pfs:** Median real-world progression-free survival.
            - **median_pfs:** Median progression-free survival.
            - **os_12_month:** 12-month overall survival rate.
            - **treatment_specific_results:** Object mapping each treatment regimen to its specific outcomes.
            - **group_difference:** Any statistical comparisons (e.g., p-values).

    ### Instructions:
    1. Parse the content in sequence, identifying the prompts from the AI (keys from the form) and the corresponding responses from the human.
    2. Match the keys in the form with the values provided in the chat history using the descriptions in the form.
    3. Dynamically adapt to any structure of the form, extracting the correct information based on the descriptions.
    4. Ensure the output is a valid JSON object with no missing or additional fields.
    5. Process the document carefully to avoid any mistakes.
    6. If a field or data element is not present, mark it explicitly as null.
    7. Your extraction must be comprehensive and handle variations in how information is presented
    8. The solution should work automatically for new"""

    def extract(self, file_content, extractor_json_schema) -> Dict:
        self.extractor_agent.set(content=file_content)
        self.extractor_agent.set(extractor_json_schema=AppUtil.load_json(f"{extractor_json_schema}_schema.json"))
        self.extractor_agent_active = self.extractor_agent.get_agent()

        output = self.extractor_agent_active.invoke(
            {"messages":[
                HumanMessage(
                    content=[
                        {"type": "text", "text": "What is the extracted information on Real-World Evidence in oncology?"}
                    ]
                )
            ]}
        )
        extracted_data = json.loads(AppUtil.remove_code_blocks(output.content))
        return extracted_data