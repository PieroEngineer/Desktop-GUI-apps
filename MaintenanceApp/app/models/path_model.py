import json
import os

from PyQt6.QtWidgets import QFileDialog

class PathModel():
    
    def __init__(self):
        self.config_file_path = r'app\config\initialization_config.json'
        self.input_path = ''
        self.output_path = ''

        self._create_config_json_path()
        self._read_and_set_path_from_json()
    
    def return_input_path(self):
        return self.input_path
        
    def return_output_path(self):
        return self.output_path
    
    def update_input_path(self):
        # In session
        file_path, _ = QFileDialog.getOpenFileName(None, "⤴️  Archivo a SUBIR al mantenimiento")
        self.input_path = file_path
        
        # In records
        try:
            with open(self.config_file_path, 'r') as f:
                data = json.load(f)
            data['paths']['last_input_file_path'] = file_path
            with open(self.config_file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f'‼️ There was a problem saving json | {e}\n')
            pass

    def update_output_path(self):
        # In session
        folder_path = QFileDialog.getExistingDirectory(None, "💾  Carpeta donde se GUARDARÁ el mantenimiento")
        self.output_path = folder_path
        
        # In records
        try:
            with open(self.config_file_path, 'r') as f:
                data = json.load(f)
            data['paths']['last_output_folder_path'] = folder_path
            with open(self.config_file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f'‼️ There was a problem saving json | {e}\n')
            pass


    def _read_and_set_path_from_json(self):
        try:
            with open(self.config_file_path, 'r') as f:
                data = json.load(f)   

            self.input_path = data['paths']['last_input_file_path']
            self.output_path = data['paths']['last_output_folder_path']
        except Exception as e:
            print(f'‼️ There was a problem reading js | {e}\n')
            self.input_path = ''
            self.output_path = ''
            pass

    def _create_config_json_path(self):
        """
        Checks if a JSON file exists at the specified path. If not, creates the necessary folders
        and an empty JSON file.

        Parameters:
        - file_path (str): Full path to the JSON file including the file name.

        Returns:
        - bool: True if the file already existed, False if it was created.
        """
        # Check if the file already exists
        if os.path.isfile(self.config_file_path):
            return

        # Extract the directory path
        dir_path = os.path.dirname(self.config_file_path)

        # Create directories if they don't exist
        os.makedirs(dir_path, exist_ok=True)

        # Create an empty JSON file
        with open(self.config_file_path, 'w') as json_file:
            empty_paths = {
                "paths": {
                    "last_input_file_path": "",
                    "last_output_folder_path": ""
                }
            }
            json.dump(empty_paths, json_file)