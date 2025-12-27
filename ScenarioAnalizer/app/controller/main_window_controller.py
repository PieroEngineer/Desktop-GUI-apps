from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QTimer


from view.main_window import MainWindow

from model.line_model import LineModel

from view.trend_sum_window import TrendSumWindow

class MainWindowrController():
    def __init__(self, view: MainWindow, line_model: LineModel, app_controller):
        self.app_controller = app_controller
        
        # Models
        self.line_model = line_model

        # Views
        self.view = view
        
        # Connect the synchronous button signals    #TODO: Create the asynchronous signals in the thread
        self.view.add_button_local.clicked.connect(self.select_data)
        self.view.line_tabs_btn.clicked.connect(self.see_in_table)

        self.view.from_combo.currentIndexChanged.connect(self.update_trend_limits)
        self.view.to_combo.currentIndexChanged.connect(self.update_trend_limits)
        self.view.export_csv_button.clicked.connect(self.on_csv_button)

        self.view.add_manual_btn.clicked.connect(lambda: self.add_manual_nominal(self.view.manual_value_input.text()))
        
        self.view.summation_of_nominals_button.pressed.connect(self.on_sum_noms_button_pressed)
        self.view.summation_of_nominals_button.released.connect(self.on_sum_noms_button_released)
        self.view.summation_of_nominals_button.clicked.connect(self.on_sum_noms_button_clicked)
        self.view.summation_button.clicked.connect(self.on_sum_lines_button_clicked)

        # Create a QTimer for the long press detection
        self.long_press_timer = QTimer()
        self.long_press_timer.setSingleShot(True)  # We only want it to run once
        self.long_press_timer.setInterval(2000)
        self.long_press_timer.timeout.connect(self.on_long_press_sum)

        # Self variables
        self.hold_used = False


    def select_data(self):
        self.app_controller.open_data_selector()

    def see_in_table(self):
        self.app_controller.open_data_table()

    def add_data_process(self):
        # Get the last added lines
        lines_to_display: dict[str, dict] = self.line_model.get_last_added_lines()

        # Display elements in the line UI
        for line_name, line_features in lines_to_display.items():
            # Adding elements
            self.view.trend_chart.add_line(line_name, line_features['line_data'], line_features['line_color'])
            self.view.scrollable_controls.add_element(line_name, line_features['nominal'], line_features['line_color'], line_features['line_type'] == 'pf') ## In later versions, if other line types need nominal, include them in this last small comparition
            
            # Connecting buttons
            if line_features['nominal']:
                nom_btn: QPushButton | None = self.view.scrollable_controls.elements_dict[line_name][1]
                nom_btn.clicked.connect(lambda _, n=line_name: self.add_nominal(n))

            ## Improve this to don't call by position but by name (Maybe create a controller for this)
            line_dlt_btn: QPushButton = self.view.scrollable_controls.elements_dict[line_name][2]  # The "X" button is in the third position
            line_dlt_btn.clicked.connect(lambda _, n=line_name: self.remove_data(n))           
        
        # Handle combo boxes    ## See here what happend with the combobox
        min_year, max_year = self.line_model.get_year_boundaries()
        
        self.view.from_combo.addItems(list( map(str, range(min_year, max_year+1)) ))
        self.view.to_combo.addItems(list( map(str, range(min_year, max_year+1)) ))

        self.view.from_combo.setCurrentText(str(min_year))
        self.view.to_combo.setCurrentText(str(max_year))

        # Update trend
        self.update_trend_limits()

    def remove_data(self, name):
        if self.line_model.get_current_lines():

            print(f'🗑️  {name} will be removed\n')

            self.view.trend_chart.remove_line(name)
            self.view.scrollable_controls.remove_element(name)
            self.line_model.remove_line_data(name)

            self.app_controller.line_data_removed()


    # The dynamic is...
    #   First, generate in the line model
    #   Then, let app controller know that there are new data in line model (so it collects from there)
    
    def on_sum_noms_button_pressed(self):
        print("👇  Button Pressed")
        self.long_press_timer.start()

    def on_sum_noms_button_released(self):
        if self.long_press_timer.isActive():
            print("✋  Button Released - Holding not triggered")
            self.long_press_timer.stop()
        else:
            print("👋  Button Released - Holding triggered")
    
    def on_sum_noms_button_clicked(self):
        if not self.hold_used:
            print('🤏  Button just clicked')

            if self.line_model.get_current_lines():
                # Get current lines with nom
                saved_lines = self.line_model.get_current_lines()
                saved_lines_with_nom = [line_name for line_name, line in saved_lines.items() if line['nominal']]

                lines_selected, added_line_name = self.start_selective_summatory_(saved_lines_with_nom, 'Nominal de ')

                if lines_selected:
                    self.line_model.generate_line_nom_sum(lines_selected, added_line_name)
                    self.app_controller.line_data_added()
        else:
            self.hold_used = False

    def on_long_press_sum(self):
        print("🙏  Holding triggered just now")
        self.hold_used = True

        if self.line_model.get_current_lines():
            if self.line_model.generate_line_nom_sum():
                self.app_controller.line_data_added()

    def on_sum_lines_button_clicked(self):
        if self.line_model.get_current_lines():
            saved_lines = self.line_model.get_current_lines()

            lines_selected, added_line_name = self.start_selective_summatory_(saved_lines)

            if lines_selected:
                self.line_model.generate_line_sum(lines_selected, added_line_name)
                self.app_controller.line_data_added()

    def add_nominal(self, name):
        if self.line_model.get_current_lines():
            saved_lines = self.line_model.get_current_lines()
            if f'Nominal de {name}' not in saved_lines.keys():
                self.line_model.generate_nominal_line(name)  
                self.app_controller.line_data_added()       ## Maybe these lines in unnecessary in main window controller and is better use it only in data selector controller

    def add_manual_nominal(self, manual_val: str):
        if self.line_model.get_current_lines():

            manual_val_std: str = manual_val.replace(',', '.')

            if manual_val_std.replace('.', '').isdigit():
                self.line_model.generate_manual_nominal_line(float(manual_val))
                self.app_controller.line_data_added()

    def update_trend_limits(self):
            try:
                min_val = int(self.view.from_combo.currentText())
                max_val = int(self.view.to_combo.currentText())
                
                # Ensure min < max
                if min_val >= max_val:
                    self.view.warning_label.setVisible(True)
                    return  # Ignore invalid range
                
                self.view.warning_label.setVisible(False)
                self.view.trend_chart.ax.set_xlim(min_val, max_val)
                self.view.trend_chart.canvas.draw()
            except ValueError:
                pass  # Ignore if text is not an integer 


    def start_selective_summatory_(self, names_to_sum: list[str], specification: str = ''):
        print('🧮  Summatory window has been called\n')

        selective_sum_window = TrendSumWindow(names_to_sum, self.line_model.get_current_lines('names'), specification)
        selective_sum_window.exec()

        return selective_sum_window.get_input_data()    ## Consider use "del" after return to delete the dialog window instance and avoid unnnecessary memory used 
    
    def on_csv_button(self):
        self.line_model.generate_csv_file()