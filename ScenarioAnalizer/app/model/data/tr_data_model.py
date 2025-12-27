from pathlib import Path

import pandas as pd

class TrDataModel():    ## Once pf_data_model is finished, pass its similar logic here

    def __init__(self, parquet_folder_path, excel_folder_path):
        super().__init__()
        self.parquet_folder_path: Path = parquet_folder_path
        self.excel_folder_path: Path = excel_folder_path

    def get_line_data(self):
        return self.process_data_()

    def process_data_(self):
        df = self.load_data_from_local_()
        return df.set_index('Name')

    def load_data_from_local_(self):  ## Check if all names coincide

        filename = 'TR'

        # try:
        parquet_path = self.parquet_folder_path / f'{filename}.parquet'

        if filename in self.parquet_folder_path.iterdir():

            df = pd.read_parquet(parquet_path)

        else:
            excel_path = self.excel_folder_path / f'{filename}.xlsx'
            
            df_dict = pd.read_excel(excel_path, sheet_name=None)

            tr_nom_col = {  # Edit if TR excel file format has changes
                'TRX': 'Column1',
                'TRY': 'Column2',
                'TRZ': 'Column3'
            }

            df = pd.DataFrame()
            for tr_block, tr_df in df_dict.items():

                #Xtr_df.drop(0)
                tr_df = tr_df.iloc[1:]
                tr_df = tr_df.rename(columns = {tr_nom_col[tr_block]: 'nom'})


                df = pd.concat([df, tr_df[['Name', 'nom']]], ignore_index=True)

            df.to_parquet(parquet_path, index=False)

        return df
        # except Exception as e:
        #     print(f'‼️ There was an error finding the TR data\nError:\n{e}')
        #     return pd.DataFrame()

    def download_data_online(self, filename):   #TODO
        pass
        ## If data is in parquet, take parquet
        ## Else, get data from excel, process it and save it as parquet