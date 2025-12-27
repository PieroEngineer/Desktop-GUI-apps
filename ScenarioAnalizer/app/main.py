import sys

from PyQt6.QtWidgets import QApplication

from controller.app_controller import AppController

def main():
    app = QApplication(sys.argv)
    ##apply_styles(app)

    # Application controller
    app_controller = AppController(app)

    app_controller.run()

if __name__ == "__main__":
    main()