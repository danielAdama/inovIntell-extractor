import wandb
import json
from datetime import datetime as dt
from pathlib import Path
from utils.app_utils import AppUtil
from document.processor import Preprocess
from typing import Dict, Any, List

class RWEExtractor:
    def __init__(self, wandb_project: str = "rwe-extraction-demo"):
        self.wandb_project = wandb_project
        self.processor = Preprocess()
        
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extraction that returns data based on filename
        """
        path = Path(pdf_path)
        filename = path.name
        file_content = AppUtil.load_pdf(path.read_bytes())
        output = self.processor.extract(file_content, "oncology")
        extracted_data = {
            "study_name": f"Study from {filename}",
            "file_name": filename,
        }
        extracted_data["metadata"]= {
            "version": "1.0",
            "description": "RWE Studies Annotations for Extraction Task",
            "created_at": dt.now().strftime('%Y-%m-%dT%H:%M')
        }
        
        extracted_data['raw_data'] = output
        print(extracted_data)
        return extracted_data

    def process_and_log(self, pdf_path: str):
        """
        Process a PDF and log results to wandb
        """
        run = wandb.init(
            project=self.wandb_project,
            config={
                "pdf_file": pdf_path,
                "extractor_version": "0.1.0"
            }
        )
        
        try:
            data = self.extract_from_pdf(pdf_path)
            wandb.log({
                "study_name": data["study_name"],
                "extracted_data": data,
                "status": "success"
            })
            output_file = Path(pdf_path).stem + "_extracted.json"
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            wandb.save(output_file)
            
        except Exception as e:
            wandb.log({
                "status": "error",
                "error_message": str(e)
            })
            raise
        
        finally:
            wandb.finish()