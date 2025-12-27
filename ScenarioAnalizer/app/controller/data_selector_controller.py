from PyQt6.QtCore import Qt, QThread

from model.line_model import LineModel

from model.data.data_repository import DataRepository

from view.data_selector_window import DataSelectorWindow

class DataSelectorController():
    def __init__(self, view: DataSelectorWindow, line_model: LineModel, app_controller):

        # Models
        self.line_model = line_model

        self.app_controller = app_controller
        
        # Views
        self.view = view

        # Initialization
        self.view.populate_tree(self.line_model.pf_name_map, 'pf')
        self.view.populate_tree(self.line_model.pit_name_map, 'pit')

        # Connections
        self.view.accept_btn.clicked.connect(self.on_data_selected)
        self.view.accept_btn.clicked.connect(self.on_selection_finished)
        

    def on_data_selected(self): # Thread starter

        # Collect selected names
        selected_elements = self.collect_selected_names_()
        used_elements = set(self.line_model.get_current_lines().keys())

        print(f'✔️  selected_elements: {selected_elements}\n')
        print(f'🗳️  used_elements: {used_elements}\n')

        # If lines selected are different to the lines already used, skip this method
        if not selected_elements.issubset(used_elements):   ## Change here, make it consider only PIT and PF elements, maybe use a filter method in selected elements

            # Repository is the worker
            self.data_repository = DataRepository()

            # Updating lines available
            new_lines = selected_elements - used_elements   ## It should be in a model (Maybe data_selector model) *
            print(f'🆕  new_lines: {new_lines}\n')

            #Xself.line_model.add_lines(new_lines)
            self.data_repository.set_target(new_lines)

            # Configuring thread
            self.data_thread = QThread()
            self.data_repository.moveToThread(self.data_thread)

            self.data_thread.started.connect(self.data_repository.load_data)

            # Connections
            self.data_repository.data_loading_completed.connect(self.on_data_ready)
            ##self.data_repository.error_getting_data.connect()

            # Clean up automatically after finish
            self.data_repository.data_loading_completed.connect(self.data_thread.quit)
            self.data_repository.data_loading_completed.connect(self.data_repository.deleteLater)
            self.data_thread.finished.connect(self.data_thread.deleteLater)

            self.data_thread.start()


    def on_selection_finished(self):
        # Hide current window
        print('✍️  User clicked finished to select\n')
        self.view.hide()

        # Open main window, but with app controller
        self.app_controller.go_to_main_window()

    def on_data_ready(self, collected_data: dict):
        self.line_model.save_new_line_data(collected_data)
        self.app_controller.line_data_added()

    def collect_selected_names_(self):  ## It should be in a model (Maybe data_selector model) *
        checked_items = set()
        for tree in [self.view.pf_tree, self.view.pit_tree]:
            root = tree.invisibleRootItem()
            for i in range(root.childCount()):
                parent = root.child(i)
                for j in range(parent.childCount()):
                    child = parent.child(j)
                    if child.checkState(0) == Qt.CheckState.Checked:
                        checked_items.add(f'{parent.text(0)} {child.text(0)}')
        print(f'🗒️  Lines selected: {checked_items}\n')
        return checked_items