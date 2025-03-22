import os
import uuid
import time
import pathlib
import json
import re
import json
from math import ceil
from PyPDF2 import PdfReader
import io
from typing import List, Dict, Any


class AppUtil:
    @staticmethod
    def load_file(path: pathlib.Path):
        with open(path, "r") as f:
            return f.read()
    
    @staticmethod
    def load_json(file_name: str) -> Dict:
        """
        Load JSON data from a file using pathlib.

        Args:
            file_name (str): The name of the JSON file.

        Returns:
            dict: The JSON data loaded from the file.
        """
        file_path = pathlib.Path(__file__).parent.parent / "forms" / file_name
        with file_path.open('r') as file:
            data = json.load(file)
        return data
    
    @staticmethod
    def load_pdf(file_bytes):
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Failed to extract PDF content: {e}")
            return None
    
    @staticmethod
    def remove_code_blocks(content: str) -> str:
        """
        Removes enclosing code block markers ```[language] and ``` from a given string.

        Remarks:
        - The function uses a regex pattern to match code blocks that may start with ``` followed by an optional language tag (letters or numbers) and end with ```.
        - If a code block is detected, it returns only the inner content, stripping out the markers.
        - If no code block markers are found, the original content is returned as-is.
        """
        pattern = r"^```[a-zA-Z0-9]*\n([\s\S]*?)\n```$"
        match = re.match(pattern, content.strip())
        return match.group(1).strip() if match else content.strip()