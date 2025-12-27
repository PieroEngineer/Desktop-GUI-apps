import os

from PyQt6.QtCore import QObject

from app.utils.path_reducer import abbreviate_path

from app.views.windows.main_window import MainWindow

from app.models.path_model import PathModel

class PathController(QObject):
    def __init__(self, model: PathModel, view: MainWindow, app_controller):
        super().__init__()
        self.model = model
        self.view = view
        self.app_controller = app_controller

        self.view.input_source_btn.clicked.connect(self.select_input_file)
        self.view.output_source_btn.clicked.connect(self.select_output_folder)

        if model.input_path:
            self.view.input_source_label.setText(abbreviate_path(self.model.input_path))
        else:
            self.view.input_source_label.setText('Por favor, selecciona un archivo excel')

        if model.output_path:
            self.view.output_source_label.setText(abbreviate_path(self.model.output_path))
        else:
            self.view.output_source_label.setText('Por favor, selecciona un folder de salida')

    def select_input_file(self):
        self.model.update_input_path()
        if self.model.input_path:
            self.view.input_source_label.setText(abbreviate_path(self.model.input_path))

    def select_output_folder(self):
        self.model.update_output_path()
        if self.model.output_path:
            self.view.output_source_label.setText(abbreviate_path(self.model.output_path))