# ScenarioAnalizer

A small desktop GUI tool to load, visualize and combine time-series data (PF / PIT / TR) for scenario analysis. Built with PyQt6 and pandas. The app helps pick data files, add nominal lines, sum lines, inspect numeric tables and export CSV outputs.

---

## Features
- Browse and select PF and PIT data from Excel files.
- Automatic caching to parquet for faster subsequent loads.
- Visual trend chart with multiple lines and color management.
- Add manual nominal lines and compute sums (selective or total).
- Export concatenated data to CSV.
- Table view with filterable types (PF/PIT/etc).
- Non-blocking data loading via background threads.

---

## Quick start

Prerequisites
- Python 3.9+
- Recommended: create a virtual environment

Run
- Launch the application from your IDE or the project's entry script (e.g., run the main file that initializes QApplication and AppController).  
  Note: The repository's entrypoint file may be named differently; run the file that creates QApplication and AppController.

---

## Project layout (important files)
- app/controller: controllers for main window, data selector, table, and app wiring.
- app/model: logic for PF, PIT and TR data models, and LineModel for current lines and operations.
- app/view: PyQt6 dialogs/widgets (main window, data selector, table, custom widgets).
- app/resources: data folders and CSV output location.
  - app/resources/data_excel/<pf|pit|tr>  - Place source Excel files here.
  - app/resources/data_parquet/<pf|pit|tr> - parquet cache generated automatically.
  - app/resources/csv_output - CSV files exported by the app.

---

## Data expectations & placement
- The app auto-creates the `data_excel` and `data_parquet` folders if missing and will open the Excel folder for you to drop files in.
- PF: expects Excel files with columns including "Power column" and "Año".
- PIT: expects a specific layout — code extracts classification and year columns (see PitDataModel).
- TR: aggregated nominal values extracted from a TR workbook structure (see TrDataModel).
- After dropping Excel files, press "Aceptar" in the selector so the repository converts/reads files into parquet and loads them.

---

## Usage summary
- Open "Local" to choose PF/PIT items (group → items). Use the search box to filter assets in real time.
- Selected items are loaded in background thread (non-blocking). Progress done via signals.
- In main window, add nominal lines (from TR), manual nominals, or compute sums:
  - Short click on "Suma nominales" opens a selection dialog; long press triggers total nominal sum.
- View data table and filter displayed rows by type.

---

## Notes for developers
- DataRepository spawns a thread and emits `data_loading_completed` with the loaded dict to LineModel.
- LineModel handles merging lines, creating manual lines, summations and CSV concatenation.
- TableController dynamically creates filter checkboxes and applies filters on change.
- Add/modify data model parsing for different Excel formats in app/model/data/*.

---

## Troubleshooting
- If data is not found: check `app/resources/data_excel/<type>` contains properly formatted Excel files.
- For missing nominals: TR entries are matched by line name index; missing rows will return None and log a warning.
- In upcoming versions,  data retrieving will not be run on the main thread, in order to make the application run more smoothly.

---

## Credits 
Program coded by Piero Olivas
