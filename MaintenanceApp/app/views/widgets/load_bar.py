from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QProgressBar, QLabel)


class LoadBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Load Bar Example")
        self.setGeometry(100, 100, 300, 150)

        # Layouts
        self.layout = QVBoxLayout()

        self.context_layout = QHBoxLayout()
        self.progress_layout = QHBoxLayout()

        self.layout.addLayout(self.context_layout)
        self.layout.addLayout(self.progress_layout)

        #
        self.progress_value = 0

        # LoadBar tittle
        self.tittle = QLabel()
        self.tittle.setText(f'Títutlo de barra aquí')
        self.context_layout.addWidget(self.tittle)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_layout.addWidget(self.progress_bar)

        # Program 
        self.current_total_pendings = 0

        self.setLayout(self.layout)

    def update_tittle(self, new_tittle):
        self.tittle.setText(new_tittle)

    def set_data_amount(self, data_amount):
        self.current_total_pendings = data_amount

    def reset_loading(self):
        self.progress_value = 0
        self.progress_bar.setValue(self.progress_value)

    def update_progress(self, current_load):
        if self.progress_value <= 100:
            self.progress_value = 100*(current_load / self.current_total_pendings)
            self.progress_bar.setValue(int(self.progress_value))

    def fill_bar(self):
        self.progress_bar.setValue(100)

    def start_indeterminate(self):
        # Range makes QProgressBar show the busy animation
        self.progress_bar.setRange(0, 0)

    def stop_indeterminate(self):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)