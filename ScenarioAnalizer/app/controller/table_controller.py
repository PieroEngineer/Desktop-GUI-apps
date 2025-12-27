from model.line_model import LineModel
from view.table_window import TableWindow

class TableController:
    def __init__(self, line_model: LineModel, table_view: TableWindow):
        
        self.line_model = line_model
        self.table_view = table_view

    def apply_filters(self):

        print(f'🔎  Apply filters called by checkbox change')

        # Get name of the actived line types
        actived_types = [
            available_checkbox.text() 
            for available_checkbox in self.table_view.get_current_available_filters() 
            if available_checkbox.isChecked()
        ]

        # Get data that matches with the filter
        data_filtered = {
            line_name : line_features['line_data']                                            ## Should it be in the model?
            for line_name, line_features in self.line_model.get_current_lines().items() 
            if line_features['line_type'] in actived_types
        }

        print(f'🚦  Filter modified, the current active types are {actived_types}\n')
            
        self.table_view.update_filtered_data(data_filtered)

    def update_data(self):
        self.table_view.update_available_filters(set(self.line_model.get_current_lines('line_type').values()))
        
        for filter_checkbox in self.table_view.get_current_available_filters():
            filter_checkbox.stateChanged.connect(self.apply_filters)

        self.apply_filters()