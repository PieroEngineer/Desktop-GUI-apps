from PyQt6.QtWidgets import (QDialog, QVBoxLayout,
QLabel, QLineEdit, QCheckBox, QPushButton)

from PyQt6.QtGui import QCloseEvent

class TrendSumWindow(QDialog):
    """
    A custom QDialog with a label, line edit, and a dynamic list of checkboxes.
    """
    def __init__(self, checkbox_items: list, occupied_names = [], just_visual_specification: str = ''):
        super().__init__()
        self.setWindowTitle("Suma selectiva de líneas")
        self.checkboxes: dict[QCheckBox] = {}  # Dictionary to store checkboxes for easy access
        self.main_layout = QVBoxLayout()

        self.occupied_names = occupied_names

        # Add Label and QLineEdit
        self.label = QLabel("Ingresa las líneas a sumar:")
        self.line_edit = QLineEdit('Línea nueva')
        self.line_edit.textChanged.connect(self.check_text_)
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.line_edit)

        # Add Checkboxes dynamically
        for item_text in checkbox_items:
            checkbox = QCheckBox(just_visual_specification + item_text)
            self.main_layout.addWidget(checkbox)
            self.checkboxes[item_text] = checkbox

        # Add standard OK/Cancel buttons
        self.accept_btn = QPushButton("Sumar")
        self.accept_btn.clicked.connect(self.accept)
        
        self.main_layout.addWidget(self.accept_btn)

        # Advertisements labes
        self.occupied_ads = QLabel()
        self.occupied_ads.setStyleSheet("color: red")

        self.main_layout.addWidget(self.occupied_ads)

        self.check_text_(self.line_edit.text())

        # Stablishing layout
        self.setLayout(self.main_layout)

    def check_text_(self, text):
        """Checks the line edit content and locks/unlocks the button."""
        if text:
            if text in self.occupied_names:
                self.accept_btn.setEnabled(False) 
                self.occupied_ads.setText('Nombre ocupado')
                self.occupied_ads.setVisible(True) 
            else:
                self.accept_btn.setEnabled(True)  
                self.occupied_ads.setText('Nombre ocupado')
                self.occupied_ads.setVisible(False)
        else:
            self.accept_btn.setEnabled(False)
            self.occupied_ads.setText('Nombre vacío')
            self.occupied_ads.setVisible(True) 

    def get_input_data(self):
        line_edit_text = self.line_edit.text()
        checked_items = [name for name, checkbox in self.checkboxes.items() if checkbox.isChecked()]

        print(f'🗳️  requested lines to be added are: {checked_items}\n')

        return checked_items, line_edit_text
    
    def closeEvent(self, event: QCloseEvent):
        """Handle the close event of the dialog."""

        print(f'🫸  Summatory canceled by user\n')

        for checkbox_used in self.checkboxes.values():
            checkbox_used.setChecked(False)

        event.accept()
    