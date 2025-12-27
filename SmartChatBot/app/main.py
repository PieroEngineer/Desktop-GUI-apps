from PyQt6.QtWidgets import QApplication

import sys

from views.main_window import MainWindow
from controllers.chatbot_controller import ChatbotController

__version__ = "1.0.0"
__author__ = "Piero Olivas"
__credits__ = ['Piero Olivas']
__maintainer__ = "Piero Olivas"
__email__ = "polivas@rep.com.pe"
__copyright__ = "Copyright (C) 2024 Red de Energía del Perú S.A."

def main():
    app = QApplication(sys.argv)

    # Views
    main_window = MainWindow()

    # Controllers
    chat_controller = ChatbotController(main_window)

    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()