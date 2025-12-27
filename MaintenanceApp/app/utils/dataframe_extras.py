import pandas as pd

def insert_new_rows(df_base, new_df_piece, insertion_pos):
    df_new = pd.concat([df_base.iloc[:insertion_pos], new_df_piece, df_base.iloc[insertion_pos:]]).reset_index(drop=True)
    return df_new