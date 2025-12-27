from PyQt6.QtCore import QObject, pyqtSignal

from pathlib import Path

import pandas as pd
import os

from utils.ads_dialog import show_ads

from model.data.tr_data_model import TrDataModel
from model.data.pf_data_model import PfDataModel
from model.data.pit_data_model import PitDataModel


class DataRepository(QObject):
    data_loading_completed = pyqtSignal(dict)
    error_getting_data = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.data_base_path = Path(r'app\resources')

        self.pf_parquet_path = self.data_base_path / r'data_parquet\pf_data'
        self.pf_excel_path = self.data_base_path / r'data_excel\pf_data'

        self.pit_parquet_path = self.data_base_path / r'data_parquet\pit_data'
        self.pit_excel_path = self.data_base_path / r'data_excel\pit_data'
        
        self.tr_parquet_path = self.data_base_path / r'data_parquet\tr_data'
        self.tr_excel_path = self.data_base_path / r'data_excel\tr_data'

        for path in [self.pf_parquet_path, self.pf_excel_path, self.pit_parquet_path, self.pit_excel_path, self.tr_excel_path, self.tr_parquet_path]:
            match path:
                case _ if 'pit' in str(path):
                    nom = 'PIT'
                case _ if 'TR' in str(path):
                    nom = 'TR'
                case _ if 'pf' in str(path):
                    nom = 'PF'    
                case _:
                    nom = '<El programa no ubicó el tipo de archivo requerido aquí>'
                
            comments = f'Por favor, colocar los archivos Excel de los {nom}\nen este folder que se acaba de abrir\n\nPresionar Aceptar cuando estén listos'
            
            if not path.exists():
                path.mkdir(parents=True)
                if 'data_excel' in str(path):
                    os.startfile(str(path))
                    show_ads(comments)
            elif not any(path.iterdir()) and 'data_excel' in str(path):
                os.startfile(str(path))
                show_ads(comments)


        self.pf_data_model = PfDataModel(self.pf_parquet_path, self.pf_excel_path)
        self.pit_data_model = PitDataModel(self.pit_parquet_path, self.pit_excel_path)
        self.tr_data_model = TrDataModel(self.tr_parquet_path, self.tr_excel_path)

        self.tr_df: pd.DataFrame = self.tr_data_model.get_line_data()

        self.current_targets = set()

    def load_data(self):
        collected_data = {}
        print(f'⚡  Thread started and self.current_targets are:\n{self.current_targets}\n')

        for current_target in self.current_targets:
            # try:
            line_type_detected = self.check_type_by_name_(current_target)
            if line_type_detected=='pit':
                collected_data[current_target] = {'line_data': self.pit_data_model.get_line_data(current_target), 'line_type': 'pit', 'nominal': None}
            elif line_type_detected=='pf':
                collected_data[current_target] = {'line_data': self.pf_data_model.get_line_data(current_target), 'line_type': 'pf', 'nominal': self.tr_df.at[current_target, 'nom']}

            print(f' 📥   For the {'PIT' if self.check_type_by_name_(current_target)=='pit' else 'PF'} line {current_target}:\n')
            # except Exception as e:
            #     print(f'‼️  There was an error in {current_target} extraction\n  -> {e}\n')
            #     self.error_getting_data.emit()# Here place the lines were there was an error
            #     pass

        self.data_loading_completed.emit(collected_data)

    def set_target(self, elements):
        self.current_targets = elements

    def check_type_by_name_(self, name):
        if name[0:5] == 'F-100':
            return 'pit'
        else:
            return 'pf'
        
    def safe_tr_searching_(self, line_name_to_search):
        if line_name_to_search in self.tr_df.index:
            return self.tr_df.at[line_name_to_search, 'nom']
        else:
            print(f'⚠️  A nominal value for {line_name_to_search} could not be found.\n')
            return None
