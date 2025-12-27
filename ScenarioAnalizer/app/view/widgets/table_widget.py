import sys
from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
import pandas as pd

class YearTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Transposed DataFrame Table")
        self.table_layout = QVBoxLayout(self)

        # Create and populate the table
        self.table = QTableWidget()
        self.populate_table_(pd.DataFrame())
        
        self.table_layout.addWidget(self.table)
        self.setLayout(self.table_layout)

    def update_data(self, new_data_dict: dict[str, pd.DataFrame] = {}):

        # Readapt the new data
        adapted_df = self.adapt_data_(new_data_dict)
        
        # Clear and repopulate the table
        self.table.clear()
        self.populate_table_(adapted_df)
        
        # Resize columns to content for better visibility
        self.table.resizeColumnsToContents()

    def adapt_data_(self, data_dict: dict[str, pd.DataFrame]) -> pd.DataFrame:  #TODO: Remove it from here and use it from model 
        # Get all unique years across DataFrames, sorted
        all_years = sorted(set(year for df in data_dict.values() for year in df['Año']))
        
        # Create a new DataFrame with rows as keys, columns as years
        result_df = pd.DataFrame(index=list(data_dict.keys()), columns=all_years)
        
        # Fill values for each DataFrame
        for name, df in data_dict.items():
            # Create Series with years as index, values as 'S HV [MVA]'
            series = pd.Series(df['S HV [MVA]'].values, index=df['Año'])    ## Avoid call 'S HV [MVA]', try to make  
            # Reindex to all years, fill missing with '-'
            result_df.loc[name] = series.reindex(all_years).fillna('-')
        
        return result_df

    def populate_table_(self, adapted_df: pd.DataFrame):
        # Set row and column counts
        self.table.setRowCount(len(adapted_df.index))
        self.table.setColumnCount(len(adapted_df.columns))
        
        # Set horizontal headers (years as strings)
        self.table.setHorizontalHeaderLabels([str(year) for year in adapted_df.columns])
        
        # Set vertical headers (dataframe names)
        self.table.setVerticalHeaderLabels(adapted_df.index.tolist())
        
        # Populate cells
        for row_idx, row_name in enumerate(adapted_df.index):
            for col_idx, year in enumerate(adapted_df.columns):
                value = adapted_df.loc[row_name, year]
                item = QTableWidgetItem(str(round(float(value), 3)) if isinstance(value, float) else value)
                self.table.setItem(row_idx, col_idx, item)