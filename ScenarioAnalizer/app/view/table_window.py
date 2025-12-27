import pandas as pd

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QCheckBox

from view.widgets.table_widget import YearTableWidget

class TableWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tabla de valores")
        self.setMinimumSize(1100, 350)

        # Self Variables
        self.current_available_filters: list[QCheckBox]= [] 
        self.actived_filters: list[QCheckBox]= []

        # Main layout
        self.main_layout = QVBoxLayout()

        self.filter_layout = QHBoxLayout()
        self.table_layout = QHBoxLayout()

        self.main_layout.addLayout(self.filter_layout)
        self.main_layout.addLayout(self.table_layout)

        # Building main layout
        self.filters_ui()
        self.table_ui()

        # Stablishing layout
        self.setLayout(self.main_layout)

    #--UI methods--------
    def filters_ui(self):
        self.update_available_filters(set())

    def table_ui(self):
        self.table = YearTableWidget()

        self.table_layout.addWidget(self.table)

    #--Mechanical methods--------
    def update_available_filters(self, filters_to_show: set):

        if self.current_available_filters:

            # Delete previous filters
            for i in range(self.filter_layout.count() - 1, -1, -1):
                item = self.filter_layout.itemAt(i)
                widget = item.widget()
                # Ensure it's a QCheckBox and not one of the control buttons
                if isinstance(widget, QCheckBox):
                    self.filter_layout.removeWidget(widget)
                    widget.deleteLater() # Schedule for deletion
            # Clean data    // |X -> Should it be before checkbox objects deletition
            self.current_available_filters = []

        # Create new filters (the connection is controller)
        for option in filters_to_show:
            checkbox = QCheckBox(option)
            checkbox.setChecked(True)   ## Here or in controller?
            self.filter_layout.addWidget(checkbox)

            self.current_available_filters.append(checkbox)
            ## Save in actived here too?

    def get_current_available_filters(self):
        return self.current_available_filters
    
    def update_filtered_data(self, lines_data: dict[str, pd.DataFrame]):

        self.table.update_data(lines_data)