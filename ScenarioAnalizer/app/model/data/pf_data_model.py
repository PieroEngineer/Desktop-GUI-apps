import pandas as pd

from pathlib import Path


class PfDataModel():

    def __init__(self, parquet_folder_path, excel_folder_path):
        super().__init__()
        self.parquet_folder_path: Path = parquet_folder_path
        self.excel_folder_path: Path = excel_folder_path

    def get_line_data(self, data_name) -> pd.DataFrame:
        
        filename = data_name 
        df = self.load_data_from_local_(filename)

        return self.process_data_(df)

    def process_data_(self, df: pd.DataFrame):
        try:
            df = df[["Power column", "Año"]].copy()
            df['Año'] = df['Año'].astype(int)
            df = df.groupby("Año")["Power column"].max().reset_index()
        except Exception as e:
            print(f'‼️ There was an error processing the PF data\nError:\n{e}')
            return pd.DataFrame()
        return df

    def load_data_from_local_(self, filename):

        try:
            parquet_path = self.parquet_folder_path / f'{filename}.parquet'

            if filename in self.parquet_folder_path.iterdir():

                df = pd.read_parquet(parquet_path)     #TODO: Verify if extension is needed

            else:
                excel_path = self.excel_folder_path / f'{filename}.xlsx'
                df = pd.read_excel(excel_path)

                df.to_parquet(parquet_path, index=False)

            return df
        except Exception as e:
            print(f'‼️ There was an error finding the PF data\nError:\n{e}')
            return pd.DataFrame()

    def download_data_online(self, filename):
        pass
        ## If data is in parquet, take parquet
        ## Else, get data from excel, process it and save it as parquet