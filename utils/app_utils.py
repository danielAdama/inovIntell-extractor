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
    
    @staticmethod
    def split_text_into_chunks(text: str, max_chunk_size: int = 5900) -> list:
        """
        Splits the input text into chunks of approximately max_chunk_size characters.
        This simple approach splits at newline characters if possible to avoid breaking sentences.
        """
        lines = text.split('\n')
        chunks = []
        current_chunk = ""
        for line in lines:
            # If adding the next line exceeds the max_chunk_size, save current chunk and start a new one
            if len(current_chunk) + len(line) + 1 > max_chunk_size:
                chunks.append(current_chunk.strip())
                current_chunk = line + "\n"
            else:
                current_chunk += line + "\n"
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        return chunks
    
    @staticmethod
    def extract_with_chunking(preprocess_instance, file_content: str, extractor_json_schema: str) -> List[Dict]:
        """
        Splits the content into chunks and processes each chunk using the provided
        preprocess_instance's extract method.
        """
        chunks = AppUtil.split_text_into_chunks(file_content)
        aggregated_results = []
        for idx, chunk in enumerate(chunks):
            print(f"Processing chunk {idx + 1} of {len(chunks)}")
            try:
                result = preprocess_instance.extract(chunk, extractor_json_schema)
                time.sleep(0.8)  # Delay to avoid overloading the context or API
                aggregated_results.append(result)
            except Exception as e:
                print(f"Error processing chunk {idx + 1}: {e}")
        return aggregated_results

    @staticmethod
    def summarize_with_chunking(preprocess_instance, file_content: str) -> List[Dict]:
        """
        Splits the content into chunks and processes each chunk using the provided
        preprocess_instance's extract method.
        """
        chunks = AppUtil.split_text_into_chunks(file_content)
        aggregated_results = []
        for idx, chunk in enumerate(chunks):
            print(f"Processing chunk {idx + 1} of {len(chunks)}")
            try:
                result = preprocess_instance.summarize(chunk)
                time.sleep(1)  # Delay to avoid overloading the context or API
                aggregated_results.append(result)
            except Exception as e:
                print(f"Error processing chunk {idx + 1}: {e}")
        return aggregated_results