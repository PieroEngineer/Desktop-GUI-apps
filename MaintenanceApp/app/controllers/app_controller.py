from app.views.windows.main_window import MainWindow
from app.views.windows.about_window import AboutWindow

from app.models.path_model import PathModel

from app.controllers.path_controller import PathController
from app.controllers.process_controller import ProcessController

class AppController:
    def __init__(self, main_window: MainWindow, about_window: AboutWindow):

        # Views
        self.main_window = main_window
        self.about_window = about_window

        # Models
        self.path_model = PathModel()

        # Controllers
        self.path_controller = PathController(self.path_model, self.main_window, self)
        self.process_controller = ProcessController(self.path_model, main_window, self) 

        # Navigation
        self.main_window.info_btn.clicked.connect(self.on_info_btn_clicked)
        self.about_window.accept_btn.clicked.connect(self.about_window.hide)

    def on_info_btn_clicked(self):
        self.about_window.show()

        