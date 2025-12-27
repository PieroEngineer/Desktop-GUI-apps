import sys

from model.line_model import LineModel

from view.main_window import MainWindow
from view.data_selector_window import DataSelectorWindow
from view.table_window import TableWindow

from controller.data_selector_controller import DataSelectorController
from controller.main_window_controller import MainWindowrController
from controller.table_controller import TableController

class AppController:
    def __init__(self, app):
        self.app = app

        # Models
        self.line_model =  LineModel()

        # Views
        self.data_selector_view = DataSelectorWindow()
        self.main_view = MainWindow()
        self.table_view = TableWindow() #TODO: In order to make the app's initialization faster, it should be created when the main_view is started, not here

        # Controllers
        self.data_selector_controller = DataSelectorController(self.data_selector_view, self.line_model, self)
        self.main_view_controller = MainWindowrController(self.main_view, self.line_model, self)
        self.table_controller = TableController(self.line_model, self.table_view)

        # Connections
        self.data_selector_view.finished.connect(self.finish_app_from_selector)

    def run(self):  # App starter method
        self.open_data_selector()
        sys.exit(self.app.exec())

    #--Navigation
    def open_data_selector(self):
        self.data_selector_view.exec()  ## .show() if you don't want to block the main
        self.data_selector_view.uncheck_all()

    def open_data_table(self):
        self.table_view.exec()
        
    def go_to_main_window(self):
        # Open the main window with app_controller
        if not self.main_view.isVisible():
            self.main_view.show()

    def line_data_added(self):
        self.main_view_controller.add_data_process()
        self.table_controller.update_data()
        print('♻️  Line updating (By adding) was requested\n')

    def line_data_removed(self):
        self.table_controller.update_data()
        ## The main controller go here too to remove a line (For now, it's being handled in the self main controller)
        print('♻️  Line updating (By removing) was requested\n')

    def finish_app_from_selector(self):
        print('🔙  Finished has been called\n')
        if not self.main_view.isVisible():
            sys.exit(0)

        