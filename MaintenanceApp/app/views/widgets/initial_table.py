from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt


class InitialTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_table()

    def _setup_table(self):
        """Configure table appearance and behavior."""
        self.setAlternatingRowColors(True)  # Improve readability
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Read-only
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setSortingEnabled(True)

    def clear_table(self):
        """Clear all contents and reset row/column count."""
        self.clear()
        self.setRowCount(0)
        self.setColumnCount(0)

    def update_table(self, data_tuples):  ## It's better include this method in the parallel thread
        """
        Update the table from a list of tuples: (name_string, dataframe)
        Row layout:
            [0] -> number of dataframe rows
            [1] -> the tuple string
            [2..] -> dataframe column names
        """
        # Clear current contents
        self.clear_table()

        # Prepare new content
        row_count = len(data_tuples)
        self.setRowCount(row_count)

        # Determine max number of columns needed
        max_cols = 2  # For count + name
        for _, df in data_tuples:
            max_cols = max(max_cols, 2 + len(df.columns))
        self.setColumnCount(max_cols)

        # Fill table
        for row, (name, df) in enumerate(data_tuples):
            # Column 0: row count of df
            self.setItem(row, 0, QTableWidgetItem(str(len(df))))
            # Column 1: name string
            self.setItem(row, 1, QTableWidgetItem(str(name)))
            # Remaining columns: dataframe column names
            for i, col_name in enumerate(df.columns, start=2):
                self.setItem(row, i, QTableWidgetItem(str(col_name)))
