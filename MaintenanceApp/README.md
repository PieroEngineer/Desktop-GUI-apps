# MaintenanceApp

MaintenanceApp is a PyQt6 desktop utility to load Excel data exported from energy measurement devices, clean and repair time-series gaps, optionally enrich missing voltage data from a PME (remote SQL) source, and save the processed results as per-sheet Excel files. The UI is Spanish-focused (labels, messages) and is intended for small teams or personal workflows that need reproducible pre- and post-processing of meter data.

## Main features
- Load an Excel workbook with multiple sheets and convert sheets to pandas DataFrames.
- Data cleaning pipeline with steps such as:
  - Remove empty columns, normalize datetime column, rename/normalize column names.
  - Detect and fill small gaps ("hipos" — single 15-min gaps) and larger missing intervals ("sneeze") by inserting rows or averaging neighboring values.
  - Handle voltage column naming and optionally fetch missing voltage data from PME via ODBC.
  - Round very small numbers to readable precision and reorder columns to expected schema.
- Threaded processing (QThread) with real-time log messages, step indicator, and progress/load bar in the UI.
- Export processed sheets to individual Excel files into a chosen output folder.
- Save a timestamped log file with processing messages.

## Tech stack & dependencies
- Python 3.8+
- PyQt6 (GUI)
- pandas (data manipulation)
- pyodbc (optional: fetch missing values from PME SQL Server)
- openpyxl / xlrd (Excel file reading)
- Other small utilities in app/utils

Install dependencies (if repository has requirements.txt):
```
pip install -r requirements.txt
```

Or install minimal deps:
```
pip install pyqt6 pandas pyodbc openpyxl xlrd
```

## Quick start
1. Clone the repo:
   ```
   git clone <repo-url>
   ```
2. Create & activate a virtual env (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate   (Windows)
   ```
3. Install dependencies (see above).
4. Run the app from the project root:
   ```
   python -m app.main
   ```
   or
   ```
   python app\main.py
   ```

## Typical workflow (UI)
1. Click "Selecciona archivo" to choose the input Excel workbook.
2. Click "Selecciona dónde se guardará" to choose the output folder.
3. (Optional) Enable "Acceso a PME" if you want the app to try fetching missing voltage values — note: requires ODBC Driver 18 and valid PME credentials.
4. Click "Tratamiento de datos" to start processing. Follow logs and step indicator.
5. When complete, processed per-sheet Excel files are saved in the chosen output folder and a timestamped log is available.

## Configuration & PME / ODBC notes
- App stores recent file/folder paths in: app/config/initialization_config.json
- Mapping for PME source names is in: app/config/pme_names_related.json (used to map sheet/device names for SQL queries)
- The SQL connection string used in the code contains placeholders:
  SERVER, DATABASE, UID, PWD — you must update these values in app/models/process_model.py (handle_vll_data_missing) to match your PME environment, or implement environment-variable injection for security.
- ODBC Driver 18 for SQL Server is recommended/required if you enable "Acceso a PME". The UI shows a reminder label to install the driver when the checkbox is toggled.

## Internals / file map (important files)
- app/main.py — application entrypoint, sets up QApplication and AppController.
- app/controllers/
  - app_controller.py — wires models/controllers/views and about window.
  - path_controller.py — handles selecting input/output paths and label updates.
  - process_controller.py — creates ProcessModel, runs it in a QThread, connects signals to UI.
- app/models/
  - path_model.py — manages persisted input/output paths (JSON).
  - process_model.py — data conversion and the full processing pipeline (core logic).
- app/views/ — windows, widgets, step indicator, load bar, tables and log block used by UI.
- app/resources/QSS.py — app-wide stylesheet.

## Logs and outputs
- Processed per-sheet Excel files are saved to the selected output folder with the sheet name as filename.
- A timestamped log text file is written to the output folder and auto-opened at the end of processing.

## Troubleshooting
- "Driver 18" reminder: install Microsoft ODBC Driver 18 for SQL Server if you plan to use PME fetching.
- If PME fetch returns empty or errors, verify credentials and the SQL query parameters inside app/models/process_model.py.
- For Excel read errors, ensure correct engines are installed (openpyxl for .xlsx, xlrd for .xls).

---

## Credits 
Program coded by Piero Olivas