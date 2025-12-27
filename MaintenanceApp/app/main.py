# src/main.py (modified)
import sys

from PyQt6.QtGui import QFont

from PyQt6.QtWidgets import QApplication

from app.controllers.app_controller import AppController

from app.views.windows.main_window import MainWindow
from app.views.windows.about_window import AboutWindow

from app.resources.QSS import QSS

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    app.setFont(QFont("Inter", 8))  # or "Segoe UI", "Roboto"

    main_window = MainWindow()
    about_window = AboutWindow()

    app_controller = AppController(main_window, about_window)
 
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()