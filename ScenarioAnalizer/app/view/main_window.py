from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QComboBox, QLabel, QHBoxLayout,
    QFrame, QLineEdit, QScrollArea
)

#from matplotlib.backends.backend_qt5 import NavigationToolbar2QT

from view.widgets.trend_chart_widget import TrendChartWidget
from view.widgets.line_scroll_widget import LineScrollWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador de escenarios")
        self.setMinimumSize(1250, 650)
        self.setWindowFlags(Qt.WindowType.Window)

        # General layouts
        self.main_layout = QVBoxLayout()
        
        self.summarizers_layout = QHBoxLayout()
        self.line_layout = QVBoxLayout()
        self.range_layout = QHBoxLayout()

        self.thin_line = QFrame()

        self.adding_layout = QHBoxLayout()

        self.main_layout.addLayout(self.summarizers_layout, stretch=1)
        self.main_layout.addLayout(self.line_layout, stretch=6)
        self.main_layout.addLayout(self.range_layout, stretch=1)
        self.main_layout.addWidget(self.thin_line)
        self.main_layout.addLayout(self.adding_layout, stretch=1)

        # Building main layout
        self.summarizers_ui()
        self.line_ui()
        self.date_range_ui()

        self.thin_line.setFrameShape(QFrame.Shape.HLine)
        self.thin_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.thin_line.setLineWidth(1)

        self.adding_ui()

        # Set final layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)


    def summarizers_ui(self):   ## Contine here: include the tool bar. in the test folder "toolbar" there is one working 
        self.export_csv_button = QPushButton("📄 Exportar CSV")
        self.export_csv_button.setFixedWidth(120)

        self.line_tabs_btn = QPushButton("🗺️ Ver valores en tablas")
        self.line_tabs_btn.setFixedWidth(200)

        ##self.summarizers_layout.addWidget(self.toolbar)
        self.summarizers_layout.addWidget(self.export_csv_button)
        self.summarizers_layout.addStretch(1)
        self.summarizers_layout.addWidget(self.line_tabs_btn)

    def line_ui(self): ## Canvas here
        self.trend_chart = TrendChartWidget()

        # Assemble right side for station controls
        self.scrollable_controls = LineScrollWidget()

        self.line_layout.addWidget(self.trend_chart, stretch=8)
        self.line_layout.addWidget(self.scrollable_controls, stretch=2)

    def date_range_ui(self):
        self.from_combo = QComboBox()
        self.from_combo.setFixedWidth(80)

        self.to_combo = QComboBox()
        self.to_combo.setFixedWidth(80)

        self.warning_label = QLabel("Desde >= Hasta?")
        self.warning_label.setVisible(False)
        self.warning_label.setStyleSheet("color: red")

        self.range_layout.addWidget(QLabel("Desde:"))
        self.range_layout.addWidget(self.from_combo)

        self.range_layout.addStretch(1)
        self.range_layout.addWidget(self.warning_label)

        self.range_layout.addWidget(QLabel("Hasta:"))
        self.range_layout.addWidget(self.to_combo)

    def adding_ui(self):
        self.manual_value_input = QLineEdit()
        self.manual_value_input.setValidator(QDoubleValidator())
        self.manual_value_input.setFixedWidth(80)

        self.add_manual_btn = QPushButton("🫳 Añadir")
        self.add_manual_btn.setFixedWidth(80)

        self.add_button_local = QPushButton("📂 Local")
        self.add_button_local.setFixedWidth(90)

        self.add_button_cloud = QPushButton("☁️ Sharepoint")
        self.add_button_cloud.setFixedWidth(90)

        self.summation_button = QPushButton("🧮 Suma líneas")
        self.summation_button.setFixedWidth(110)

        self.summation_of_nominals_button = QPushButton("➕ Suma nominales")
        self.summation_of_nominals_button.setFixedWidth(120)

        self.adding_layout.addWidget(QLabel("Valor nominal manual = "))
        self.adding_layout.addWidget(self.manual_value_input)
        self.adding_layout.addWidget(self.add_manual_btn)

        self.adding_layout.addStretch()

        self.adding_layout.addWidget(QLabel("Obtener datos de: "))
        self.adding_layout.addWidget(self.add_button_local)
        self.adding_layout.addWidget(self.add_button_cloud)
        self.adding_layout.addWidget(self.summation_button)
        self.adding_layout.addWidget(self.summation_of_nominals_button)

    def create_scrollable_lines_list(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(550)  ## Adjust height as needed

        container = QWidget()
        self.line_controls = QVBoxLayout(container)
        self.line_controls.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll_area.setWidget(container)
        return self.scroll_area