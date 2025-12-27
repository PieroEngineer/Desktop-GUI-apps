from PyQt6.QtCore import QObject
from pathlib import Path
import pandas as pd

import datetime
import random
import os

from resources.nominations.name_map import PF_NAMES, PIT_NAMES


class LineModel(QObject):
    
    def __init__(self):
        super().__init__()
        self.pf_name_map = PF_NAMES
        self.pit_name_map = PIT_NAMES

        self.available_colors = ('#4D4D4D', '#00B140', '#FFB81C', '#FE5000', '#003087', '#0099FF')
        self.used_colors = []

        self.current_lines: dict[str, dict] = {}

        self.new_lines: dict[str, dict] = {}

        self.lines_to_sum: list[str] = []

        self.current_manual_count: int = 1
        self.current_total_sum_count: int = 1

        self.csv_path = Path(fr'app\resources\csv_output')

        starting_year = 2025
        self.n_prefixed_years_for_nominals = 11
        self.prefixed_years_for_nominals = list(range(starting_year, starting_year + self.n_prefixed_years_for_nominals))

    #--API methods---

    def save_new_line_data(self, new_line_data: dict[str, dict]):
        for line_name, line_features in new_line_data.items():
            if line_name not in self.current_lines.keys():  ## This filter is already made before
                line_features['line_color'] =  self.get_color_from_type_(line_features['line_type'])

                ## More features can be added here

        self.new_lines = new_line_data
        
        self.current_lines |= new_line_data

    def generate_nominal_line(self, name: str):
        current_df: pd.DataFrame = self.current_lines[name]['line_data']
        nom_df = current_df.copy()
        nom_df['Power colum'] = self.current_lines[name]['nominal']

        nominal_line = {f'Nominal de {name}': {'line_data': nom_df, 'line_type': 'nominal', 'nominal': None}}

        self.save_new_line_data(nominal_line)

    def generate_manual_nominal_line(self, man_value: float):

        manual_nom_df = pd.DataFrame({'Año': self.prefixed_years_for_nominals, 'Power colum': [man_value]*(self.n_prefixed_years_for_nominals)})
        
        manual_nominal_line = {f'Nominal manual {self.current_manual_count}': {'line_data': manual_nom_df, 'line_type': 'manual nominal', 'nominal': None}}
        self.current_manual_count += 1

        self.save_new_line_data(manual_nominal_line)

    def generate_line_sum(self, lines_to_sum: list[str] = [], sum_name: str = ''):
        if lines_to_sum:
            dfs_to_sum: list[pd.DataFrame] = [self.current_lines[line_name]['line_data'] for line_name in lines_to_sum]
            
            sum_line_df = {sum_name: {'line_data': self.sum_dataframes_by_year_(dfs_to_sum), 'line_type': 'summatory', 'nominal': None}}
            self.save_new_line_data(sum_line_df)

            return True
        else:
            return False

    def generate_line_nom_sum(self, lines_to_sum: list[str] = [], sum_name: str = ''):
        if not sum_name:    # If it doesn't have a name assigned, it's because it is a total sum
            lines_to_sum = [line_name for line_name, line in self.current_lines.items() if line['nominal']]
            self.current_total_sum_count += 1
            sum_name = f'Suma total de nominales {self.current_total_sum_count}'
            
        if lines_to_sum:
            sum_value = sum([line['nominal'] for line_name, line in self.current_lines.items() if line_name in lines_to_sum])

            sum_nom_df = pd.DataFrame({'Año': self.prefixed_years_for_nominals, 'Power colum': [sum_value]*(self.n_prefixed_years_for_nominals)})
            sum_nominal_line = {sum_name: {'line_data': sum_nom_df, 'line_type': 'manual nominal', 'nominal': None}}
                
            self.save_new_line_data(sum_nominal_line)
            
            return True
        else:
            return False

    def get_last_added_lines(self):
        return self.new_lines

    def get_current_lines(self, what_return = ''):
        match what_return:
            case '':
                return self.current_lines
            case 'names':
                return list(self.current_lines.keys())
            case _:
                return {line_name: line_data[what_return] for line_name, line_data in self.current_lines.items()}

    def remove_line_data(self, line_to_remove: str):
        del self.current_lines[line_to_remove]

    def get_year_boundaries(self):
        max_year = 0
        min_year = 10**4
        for line_feature in self.current_lines.values():
            line_years: pd.DataFrame = line_feature['line_data']['Año']
            max_year = max(line_years.max(), max_year)
            min_year = min(line_years.min(), min_year)
        
        return min_year, max_year
    
    def generate_csv_file(self):
        if not self.csv_path.exists():
            self.csv_path.mkdir(parents=True)

        self.concatenate_data_().reset_index().to_csv(str(self.csv_path / f'escenario del {datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")}.csv'), index=False, sep = ';')

        os.startfile(str(self.csv_path))
        
    #--Internal methods---
    def get_color_from_type_(self, line_type):
        if line_type == 'pit':  ## Change to Match-case statement if there are more special cases
            return '#FF0000'
        else:
            if len(self.available_colors) == len(self.used_colors):
                self.used_colors.clear()

            color_selected = random.choice(self.available_colors)
            while color_selected in self.used_colors:
                color_selected = random.choice(self.available_colors)
            
            self.used_colors.append(color_selected)

            return color_selected
     
    def sum_dataframes_by_year_(self, dataframes_list: list[pd.DataFrame]):
        if dataframes_list:
            concatenated_df = pd.concat(dataframes_list, axis=0)

            summed_series = concatenated_df.groupby('Año').sum()
            summed_series.reset_index(inplace=True)
            
            return summed_series  
        else:
            return []
        
    def concatenate_data_(self):

        data_to_concatenate = self.get_current_lines('line_data')

        # Get all unique years across DataFrames, sorted
        all_years = sorted(set(year for df in data_to_concatenate.values() for year in df['Año']))
        
        # Create a new DataFrame with rows as keys, columns as years
        concatenated_df = pd.DataFrame(index=list(data_to_concatenate.keys()), columns=all_years)

        # Fill values for each DataFrame
        for name, df in data_to_concatenate.items():
            # Create Series with years as index, values as 'Power colum'
            series = pd.Series(df['Power colum'].values, index=df['Año']) 
            # Reindex to all years, fill missing with '-'
            concatenated_df.loc[name] = series.reindex(all_years).fillna('-')
        
        return concatenated_df