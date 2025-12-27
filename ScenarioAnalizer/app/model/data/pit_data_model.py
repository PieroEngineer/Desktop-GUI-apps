from pathlib import Path

import pandas as pd

class PitDataModel():    ## Once pf_data_model is finished, pass its similar logic here

    def __init__(self, parquet_folder_path, excel_folder_path):
        super().__init__()
        self.parquet_folder_path: Path = parquet_folder_path
        self.excel_folder_path: Path = excel_folder_path

    def get_line_data(self, data_name) -> pd.DataFrame:
        
        filename = data_name

        return self.load_data_from_local_(filename)   # Here data is load and not process like pf because the name is needed for the process

    def process_data_(self, df: pd.DataFrame, area):
        # try:
        df = df.groupby('Classification column').sum()
        df: pd.DataFrame = df.loc[area].reset_index()

        df.columns = ['Año', 'Power colum']
        df['Año'] = df['Año'].astype(int)
        # except Exception as e:
        #     print(f'‼️ There was an error processing the PIT data\nError:\n{e}')
        #     return pd.DataFrame()
        
        return df

    def load_data_from_local_(self, filename):
        ## Here depends of the filename
        area = filename[20:]
        filename = filename[:19]

        # try:
        parquet_path = self.parquet_folder_path / f'{filename}.parquet'

        if filename in self.parquet_folder_path.iterdir():

            df = pd.read_parquet(parquet_path)     #TODO: Verify if extension is needed

        else:
            excel_path = self.excel_folder_path / f'{filename}.xlsx'
            
            df = pd.read_excel(excel_path, sheet_name=-1, header=6)
            used_columns = [year for year in list(df.columns) if isinstance(year, int)] + ['Classification column']
            df = df[used_columns]
            df = df.dropna(subset='Classification column')

            df.to_parquet(parquet_path, index=False)

        return self.process_data_(df, area)
        # except Exception as e:
        #     print(f'‼️ There was an error finding the PIT data\nError:\n{e}')
        #     return pd.DataFrame()

    def download_data_online(self, filename):   #TODO
        pass
        ## If data is in parquet, take parquet
        ## Else, get data from excel, process it and save it as parquet