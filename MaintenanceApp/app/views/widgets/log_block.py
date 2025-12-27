from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit
from PyQt6.QtCore import QDateTime


class LogBlock(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Read-only Text Example")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        # Create the read-only text box
        self.log_area = QPlainTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

    def add_line(self, text=None):
        """Appends a new line to the read-only text box."""
        if text is None:
            text = "New log line"
        self.log_area.appendPlainText(text)

    def clear_log(self):
        """Clears all text."""
        self.log_area.clear()

    
    def get_content(self):
        # Get the current text from the log area
        print("Log info was asked\n")
        return self.log_area.toPlainText()