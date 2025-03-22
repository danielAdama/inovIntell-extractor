# inovIntell-extractor

**inovIntell-extractor** is an NLP-based extraction tool for Real-World Evidence (RWE) studies in oncology. It parses PDF documents and extracts structured information—demographics and treatment outcomes—using custom agents and dynamic JSON schemas. The results are logged to Weights & Biases (wandb) for evaluation.

## Features

- **Two-Stage Extraction Process:**  
  - **Demographics Extraction:** Extracts treatment regimens, countries, and patient population details.
  - **Results Extraction:** Extracts treatment outcomes (e.g., median overall survival, progression-free survival, group differences) from the document.
- **Dynamic Schema-based Extraction:**  
  Uses JSON schemas to drive the extraction process, ensuring consistent and accurate output.
- **Integration with wandb:**  
  Logs extraction results and experiment configurations for easy tracking and evaluation.
- **PDF Parsing:**  
  Utilizes [PyPDF2](https://pypi.org/project/PyPDF2/) to read PDF content and process documents in chunks to avoid context window limitations.
- **Custom Agent Architecture:**  
  Built on top of a flexible agent system (using LangChain) for dynamic prompt generation and extraction.

## Project Structure

```
inovIntell-extractor/
├── agents/
│   ├── agent.py              # Agent implementation for extraction tasks.
│   └── base_agent.py         # Base class for agents.
├── config/
│   ├── app_config.yml        # Application configuration including prompt settings.
│   └── logger.py             # Logger configuration.
├── document/
│   └── processor.py          # Orchestrates extraction by invoking demographics and results agents.
├── extractor/
│   └── rwe_extractor.py      # Main extractor class that integrates document processing and wandb logging.
├── forms/
│   ├── demographics_schema.json   # JSON schema for demographics extraction.
│   └── results_schema.json          # JSON schema for results extraction.
├── utils/
│   └── app_utils.py          # Utility functions for file handling, PDF extraction, and text processing.
├── main.py                   # Command-line entry point.
├── Makefile                  # Build/run commands.
└── README.md                 # Project documentation (this file).
```

## Results
###Study from Banna 2022.pdf
![Screenshot 2025-03-22 at 22 43 25 2](https://github.com/user-attachments/assets/3c2d78c5-ee67-487c-a72e-86ec03d6df1c)
<img width="1676" alt="Screenshot 2![Screenshot 2025-03-22 at 22 46 26 2](https://github.com/user-attachments/assets/40cf0a42-ed15-4d41-9fd3-070613fe9186)
025-03-22 at 22 43 25" src="https://github.com/user-attachments/assets/0df6e47f-18de-411d-8e84-88f283d2e51d" />

###Study from Belaroussi 2023.pdf
<img width="1674" alt="Screenshot 2025-03-22 at 22 46 26" src="https://github.com/user-attachments/assets/13eb89a6-a972-4da6-a862-67fdcefeb35d" />

###Study from Pons-Tostivint 2023.pdf
![Screenshot 2025-03-22 at 22 47 30 2](https://github.com/user-attachments/assets/5dc8e438-9475-4575-a6f0-0af4e22fd3ae)
<img width="1680" alt="Screenshot 2025-03-22 at 22 47 30" src="https://github.com/user-attachments/assets/adcf6101-1139-4bb0-95ce-899ea5555e3b" />


## Setup

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) (optional, for dependency management)
- wandb account for logging (set up your API key)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/danielAdama/inovIntell-extractor.git
   cd inovIntell-extractor
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```
   ```bash
   poetry shell
   ```

3. **Set up Environment Variables:**

   Create a `.env` file in the project root (or export directly) with:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   DEFUALT_MODEL=your_preferred_openai_model
   ```

## Usage

### Command-Line

Run the extractor with:
```bash
make run PDF_PATH=/path/to/your/document.pdf
```
Or directly:
```bash
python3 main.py /path/to/your/document.pdf --wandb-project your_wandb_project_name
```

### How It Works

1. **Document Processing:**  
   The `Preprocess` class (in `document/processor.py`) initializes two extraction agents:
   - **Demographics Agent:** Extracts study demographics (treatment_regimens, countries, populations) using the JSON schema from `forms/demographics_schema.json`.
   - **Results Agent:** Extracts treatment outcomes (results) using the JSON schema from `forms/results_schema.json`.

2. **Extraction Flow:**  
   - **Step 1:** The demographics agent is invoked to process the PDF content and extract key demographic data.
   - **Step 2:** The results agent processes the same PDF content (and may optionally use the demographics output) to extract outcome data.
   - **Step 3:** The final output is a merged JSON object that contains the study name, file name, demographics, and results.

3. **Logging:**  
   The extracted data is logged to wandb for further evaluation and tracking.

## Example Output

For a document named `Banna 2022.pdf`, a correct extraction might yield:
```
{
    'treatment_regimens': ['pembrolizumab plus platinum-based chemotherapy'], 
    'countries': ['United Kingdom', 'Switzerland'], 
    'populations': [
        {'stage, histology': 'IIIB/IVA, Adenocarcinoma', 'pdl1_status': 'Negative', 'n': 164}, 
        {'stage, histology': 'IVB, Adenocarcinoma', 'pdl1_status': 'Negative', 'n': 113}, 
        {'stage, histology': 'IVB, Squamous', 'pdl1_status': 'Negative', 'n': 51}, 
        {'stage, histology': 'IVB, Mixed', 'pdl1_status': 'Positive/High', 'n': 151}
        ], 
    'results': {
        'pembrolizumab plus platinum-based chemotherapy': {
            'median_os': '12.7 months', 'median_pfs': '8.0 months', 'os_12_month': '52.2%', 
            'group_difference': 'Patients with high NLR (≥4) had significantly shorter OS (median 11.8 vs 14.9 months, p=0.02) and PFS (median 6.6 vs 9.0 months, p=0.018) than those with low values.'}
        }, 
    'study_name': 'Study from Banna 2022.pdf', 
    'file_name': 'Banna 2022.pdf'
}
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
