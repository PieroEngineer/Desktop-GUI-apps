from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt

class SummarizeTable(QTableWidget):
    def __init__(self):
        # Initialize table with 10 columns and specified headers
        super().__init__(0, 10)
        self.setHorizontalHeaderLabels([
            "# Filas", "Subestación", "Local Time", "kWh del int", "kWh rec int",
            "kVARh Q1 int", "kVARh Q2 int", "kVARh Q3 int", "kVARh Q4 int", "Vll avg mean"
        ])
        self._setup_table()

    def _setup_table(self):
        # Configure table properties
        self.setAlternatingRowColors(True)  # Improve readability
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Read-only
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Scrollable
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setSortingEnabled(False)

    def update_table(self, nm_dfs):
        self.clear_table()

        # Add rows for a list of nm_df tuples (name, DataFrame)
        for df_name, df in nm_dfs:
            row_count = df.shape[0]  # Get number of rows
            row_position = self.rowCount()
 
            self.insertRow(row_position)

            # Set row count in first column
            self.setItem(row_position, 0, QTableWidgetItem(str(row_count)))
            # Set DataFrame name in second column
            self.setItem(row_position, 1, QTableWidgetItem(df_name))

            for col_idx, col_name in enumerate(df.columns, start=2):
                self.setItem(row_position, col_idx, QTableWidgetItem(col_name))
        self.resize_columns_to_content()

    def clear_table(self):
        # Clear all rows, keep headers
        self.setRowCount(0)

    def resize_columns_to_content(self):
        # Adjust column widths to fit content
        for column in range(self.columnCount()):
            self.resizeColumnToContents(column)

    def is_empty(self):
        # Check if table has no rows
        return self.rowCount() == 0

    def get_table_data(self):
        # Return table data as list of lists
        data = []
        for row in range(self.rowCount()):
            row_data = []
            for col in range(self.columnCount()):
                item = self.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)
        return data