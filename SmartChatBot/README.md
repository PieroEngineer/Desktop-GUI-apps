# SmartChatBot (ISA)

Lightweight desktop GUI chatbot that uses a local PyQt6 interface and an AI back end (Azure / OpenAI API) to process user questions and fetch/aggregate maintenance data.

---

## Features
- Simple PyQt6-based chat UI.
- Sends user messages to an LLM (Azure/OpenAI).
- Uses tools to fetch and combine monthly maintenance data from COES (downloaded ZIPs → Excel → parquet).
- Keeps basic conversation history (app/chat_history.json).
- Basic device criteria lookups from an Excel workbook.

---

## Requirements
- Python 3.10+
- Recommended packages:
  - PyQt6
  - pandas
  - requests
  - openpyxl
  - pyarrow
  - openai (for AzureOpenAI)
  - (Optional) any other utils required by your environment

Install example:
pip install PyQt6 pandas requests openpyxl pyarrow openai

---

## Project layout (key files)
- app/views/main_window.py — GUI window and message UI
- app/controllers/chatbot_controller.py — connects view and models, manages threading
- app/models/isa_chatbot_model.py — domain logic, data fetching and parsing
- app/models/azureai_llm_model.py — interacts with Azure/OpenAI
- app/models/history_model.py — stores/loads app/chat_history.json
- app/data — directory for downloaded files and parquet files (see below)

---

## Configuration
1. Azure/OpenAI credentials:
   - Edit `app/models/azureai_llm_model.py` and set:
     - `self.endpoint` (Azure endpoint)
     - `subscription_key` (API key)
     - `api_version`
     - `self.deployment` (deployment/model name)
   - Alternatively, modify the file to read these from environment variables in your environment.

2. Local data files & folders (ensure these exist with correct names):
   - `app/chat_history.json` — initialize with `[]` if not present.
   - `app/data/Contenido/Downloaded/` — will hold downloaded ZIPs.
   - `app/data/Contenido/InParquet/` — parquet cache for monthly datasets.
   - `app/data/Criterios/criteriofinal.xlsm` — Excel with device criteria (sheet "Resumen" and expected columns).

---

## Running the app
- From the project root, run the module that launches the PyQt application (example):
  - `python -m app.main` (or run your IDE entry point that creates QApplication and the MainWindow).
- Ensure the current working directory is the project root so relative paths (app/...) resolve.

---

## Troubleshooting
- Common issues:
  - "File not found" — verify `app/chat_history.json`, required folders and `criteriofinal.xlsm` exist.
  - Azure/OpenAI errors — check endpoint, key, api_version and deployment names are correct and network connectivity works.
  - Missing dependencies — confirm pip installs completed and the environment is activated.
  - Parquet load/save problems — ensure `pyarrow` is installed.

- Logging: Most modules print helpful messages to stdout; use the console for debugging.

---

## Development notes
- Concurrency: message handling runs in a QThread (see controller), so UI remains responsive.
- To change behavior of the LLM client, modify `app/models/azureai_llm_model.py`.
- To add tools or data processing, extend `IsaChatBotModel.find_data_()` and related helper methods.

---

## Credits 
Program coded by Piero Olivas
