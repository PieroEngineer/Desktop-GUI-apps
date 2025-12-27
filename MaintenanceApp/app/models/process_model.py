from PyQt6.QtCore import QObject, pyqtSignal

from datetime import datetime, timedelta

import os
import pyodbc
import pandas as pd
import json

from app.utils.dataframe_extras import insert_new_rows 
from app.utils.datetime_extras import group_datetimes_by_proximity, get_month_boundaries_from_datetime, days_in_months

class ProcessModel(QObject):
    #--Signals for asynchronus process------------------------------------------------------------------------------------------
    excel_to_df_completed = pyqtSignal(str)
    initial_data_got = pyqtSignal(list)
    data_amount_established = pyqtSignal(int)
    month_got = pyqtSignal(str)
    operation_started = pyqtSignal(str)
    data_processed = pyqtSignal(str)
    one_more_proccesed = pyqtSignal(int)
    error_ocurred = pyqtSignal(str)
    operation_done = pyqtSignal(str)
    final_data_ready = pyqtSignal(list)
    #X df_analized = pyqtSignal(int)
    ready_for_report = pyqtSignal(list, list, dict, dict)
    excel_saved = pyqtSignal(int)
    df_to_excel_completed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.nms_dfs = []
        self.desired_columns = [
            "Local Time", "kWh del int", "kWh rec int",
            "kVARh Q1 int", "kVARh Q2 int", "kVARh Q3 int",
            "kVARh Q4 int", "Voltage colum mean"
        ]

        self.current_input_path = ''
        self.current_ouput_path = ''

        self.log_path = ''

        self.pme_names_path = r'app\config\pme_names_related.json'

        self.errors_found = []

        self.empy_volt_found = []

        self.sneezes_found = {}
        self.hipos_found = {}

        self.pme_access_enabled = False

    #--Log handling------------------------------------------------------------------------------------------
    def convert_log_info_into_txt(self, content):
        if not self.log_path:
            text_file_name = f'{datetime.now().strftime("%d_%m_%Y %H.%M.%S")}_log.txt'
            self.log_path = os.path.join(self.current_ouput_path, text_file_name)
            
            with open(self.log_path, "w", encoding="utf-8") as f:
                f.write(content)

        os.startfile(self.log_path)

    #--Path update------------------------------------------------------------------------------------------
    def update_excel_path(self, new_path):
        self.current_input_path = new_path

    def update_folder_path(self, new_path):
        self.current_ouput_path = new_path
    
    #--Excel conversion------------------------------------------------------------------------------------------
    def convertion_from_excel_to_df(self):
        result = []
        if self.current_input_path:
            try:
                # Try with xlrd for .xls
                sheets = pd.read_excel(self.current_input_path, sheet_name=None, engine='xlrd')
            except Exception:
                try:
                    # Try with openpyxl for .xlsx
                    sheets = pd.read_excel(self.current_input_path, sheet_name=None, engine='openpyxl')
                except Exception as e:
                    print(f"❌ Cannot read {self.current_input_path}: {e}")
                    return []

            for sheet_name, df in sheets.items():
                result.append((sheet_name, df))
            
            self.nms_dfs =  result[6:]
        ## Add an else to trigger a advertisement
    
    def convertion_from_df_to_excel(self):
        if self.current_ouput_path:
            for i, (name, df) in enumerate(self.nms_dfs):
                self.excel_saved.emit(i)
                df.to_excel(f'{self.current_ouput_path}\\{name}.xlsx', sheet_name = name, index=False)#, engine='xlwt')
            self.df_to_excel_completed.emit()
        ## Add an else to trigger a advertisement
    
    #--Data processing------------------------------------------------------------------------------------------
        
    def add_missing_columns(self, selected):
        """
        Receives:
        - df : The input DataFrame.
        - reference_list (list of str): The expected column names.

        Returns:
        - The updated df with all reference columns present.
        """
        nm_df = self.nms_dfs[selected]

        df = nm_df[1].copy()

        for col in self.desired_columns:
            if col not in df.columns:
                df[col] = pd.NA

        return df
    
    def keep_just_similars(self, selected):
        """
        Receives:
        - df (pd.DataFrame): Original DataFrame

        Returns:
        - pd.DataFrame: DataFrame with updated column names
        """
        nm_df = self.nms_dfs[selected]

        df = nm_df[1].copy()

        current_list = list(df.columns)
        cleaned_current_list = [col.lower().replace(" ", "") for col in current_list]

        # Build a map from original name to cleaned name
        col_map = dict(zip(current_list, cleaned_current_list))

        # Prepare the reference list to be compared
        uniformed_reference_list = [col.lower().replace(" ", "") for col in self.desired_columns]

        # Keep only columns whose cleaned name is in the reference list
        columns_to_keep = [orig for orig, cleaned in col_map.items() if cleaned in uniformed_reference_list]

        return df[columns_to_keep]
    
    def lowercase_k(self, selected):
        """

        Parameters:
        - df: Original DataFrame
        - letter: The letter to check for (uppercase expected)
        - position: The character position to check

        Actions:
        - Return pd.DataFrame: New DataFrame with renamed columns
        """
        new_columns = []

        nm_df = self.nms_dfs[selected]

        df = nm_df[1].copy()

        for col in df.columns:
            if len(col) > abs(0) and col[0] == 'K':
                # Lowercase the specified character at the given position
                col = col[:0] + 'k' + col[0 + 1:]
            new_columns.append(col)

        return df.rename(columns=dict(zip(df.columns, new_columns)))
    
    def lowercase_i(self, selected):
        """

        Parameters:
        - df: Original DataFrame
        - letter: The letter to check for (uppercase expected)
        - position: The character position to check

        Actions:
        - Return pd.DataFrame: New DataFrame with renamed columns
        """
        new_columns = []

        nm_df = self.nms_dfs[selected]

        df = nm_df[1].copy()

        for col in df.columns:
            if len(col) > abs(-3) and col[-3] == 'I':
                # Lowercase the specified character at the given position
                col = col[:-3] + 'i' + col[-3 + 1:]
            new_columns.append(col)

        return df.rename(columns=dict(zip(df.columns, new_columns)))
    
    def datatime_column_handler(self, selected):
        """
        Receives:
        - dataframe to handle its datatime columns

        Final actions:
        - Return df handled
        """
        nm_df = self.nms_dfs[selected]

        df = nm_df[1].copy()

        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                
                # Standarize format
                df[col] = df[col].dt.strftime("%d/%m/%Y %H:%M:%S")

                if col != "Local Time":
                    # rename column
                    df.rename(columns={col: "Local Time"}, inplace=True)
                    break    
                break

        return df

    def handle_holes(self, selected, sample=100):   # This sample can be any number less than 1500 (random safely)
        # Access DataFrame and its name
        nm_df = self.nms_dfs[selected]
        df = nm_df[1]#X.copy()
        data_name = nm_df[0]

        ## Find excepted dates
        # Sample date to determine month boundaries
        sample_date = df['Local Time'][sample]

        sample_date = datetime.strptime(sample_date, "%d/%m/%Y %H:%M:%S")

        days = days_in_months(sample_date)
        expected_amount = days[sample_date.month - 1] * 96

        #Xprint(f'\nexpected_amount: {expected_amount} for {data_name}')

        if len(df) < expected_amount:
            ##print(f'{data_name} does not have enought elements {len(df)}/{expected_amount}\n')
            generate_dates = lambda start, n: pd.Series(pd.date_range(start=start, periods=n, freq='15min'))

        # Convert boundaries to datetime
            start_dt, end_dt = get_month_boundaries_from_datetime(sample_date)   # Are datetime type
            
            ## Create an iterable with the expected dates
            expected_dates = generate_dates(start_dt, expected_amount)
        
            ## Create a list of rows to skip (Empty)
            rows_to_skip = []

            # Rows to register holes
            filled_sneezes = []
            filled_hipos = []
        
            ## For each expected date (With enumerate)
            for i, expected_date in enumerate(expected_dates):
                filling_content = pd.DataFrame()

                ## If i isn't in skip
                if i not in rows_to_skip and i < len(df):
                    
                    if isinstance(df.at[i, 'Local Time'], str):
                        date_found = datetime.strptime(df.at[i, 'Local Time'], "%d/%m/%Y %H:%M:%S")
                    else:
                        date_found = df.at[i, 'Local Time']

                    #Xprint(f'date_found type: {type(date_found)}\nexpected_date type: {type(expected_date)}\n')
                    hole = int((date_found - expected_date).total_seconds()/60)

                    expected_date = expected_date.strftime('%d/%m/%Y %H:%M:%S')

                    # If the hole isn't higher than 15 min, treat as hipo
                    # (For all numeric columns, half of the next one. Except 'VII avg mean' that is the average of its adjacent ones)
                    if hole == 15:   # Hipo
                        # Create a dictionary with the calculated values
                        filled_hipo = {'Local Time': expected_date}

                        filling_data = {column: df.at[i+1, column]/2
                                if column != 'Voltage colum mean' else (df.at[i+1, column] + df.at[i-1, column])/2 if i>0 else df.at[i+1, column]
                                for column in df.columns 
                                if column != 'Local Time'}
                        
                        filling_content = filled_hipo | filling_data
                        filling_content = pd.DataFrame([filling_content])

                        ## Include it in hipos records
                        #Xfilled_hipos.append(filled_hipo['Local Time'])
                        filled_hipos.append(expected_date)
                        
                    # Else, treat it as a sneeze
                    # (For all numeric column, fill it with zero)
                    elif hole > 15:  # Sneeze
                        n_missing = int(hole/15)

                        # Create a full-zeros dataframe with missing dates 
                        time_data = generate_dates(expected_date, n_missing)
                        time_data = time_data.dt.strftime("%d/%m/%Y %H:%M:%S")
                        time_data.name = 'Local Time'
                        
                        filling_content = pd.DataFrame(0, 
                                                    index=range(n_missing), 
                                                    columns=[column_nm for column_nm in df.columns 
                                                            if column_nm != 'Local Time'])
                        filling_content['Local Time'] = time_data

                        # Include it in hole records

                        filled_sneeze = time_data#X.dt.strftime("%d/%m/%Y %H:%M")
                        filled_sneeze = filled_sneeze.tolist()
                        filled_sneezes += filled_sneeze
                        
                        # Include the corrected rows in the list of rows to skip
                        rows_to_skip = list(range(i + 1, i + n_missing + 1))
                            
                    # Concatenate it in data
                    if not filling_content.empty:
                        ##print(f'filling_content\n{filling_content} \n')
                        df = insert_new_rows(df, filling_content, i)

            if filled_hipos:
                self.hipos_found[data_name] = filled_hipos

            if filled_sneezes:
                filled_sneezes = group_datetimes_by_proximity(filled_sneezes)
                self.sneezes_found[data_name] = filled_sneezes
                
            ## Consider ends of the dataframe

        ##print(f'df:\n{df.head(20)}\n\n{df.tail(20)}')

        return df

    def handle_special_similarity_columns(self, selected):
        """
        Processes the DataFrame to ensure only one column remains:
        - If both 'Voltage colum' and 'Voltage colum mean' exist, keep 'Voltage colum mean' and drop 'Voltage colum'.
        - If only one exists, keep it.
        - If neither exists, create an empty 'Voltage colum mean' column.
        """
        nm_df = self.nms_dfs[selected]

        df = nm_df[1]#X.copy()

        # Handle potential trailing whitespace in column names
        columns = [col.strip() for col in df.columns]
        df.columns = columns  # Normalize column names

        has_avg = 'Voltage colum' in df.columns
        has_avg_mean = 'Voltage colum mean' in df.columns

        if has_avg and has_avg_mean:
            df.drop(columns=['Voltage colum'], inplace=True)
        elif has_avg and not has_avg_mean:
            df.rename(columns={'Voltage colum': 'Voltage colum mean'}, inplace=True)
        elif not has_avg and not has_avg_mean:
            df['Voltage colum mean'] = 0  # Create empty column

        return df
    
    def order_columns(self, selected):
        nm_df = self.nms_dfs[selected]

        df = nm_df[1]

        
        return df[self.desired_columns]
    
    def drop_empty_columns(self, selected):
        nm_df = self.nms_dfs[selected]

        df = nm_df[1]

        return df.dropna(axis=1, how='all')
    
    def handle_vll_data_missing(self, selected, sample=100):

        def change_to_local_time(dt_str, subtract_15=False):
            # Parse to datetime
            #Xdt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")

            # Subtract 15 minutes if requested
            if subtract_15:
                dt_str -= timedelta(minutes=15)

            # Offset by -5 hours
            offset_dt = dt_str + timedelta(hours=5, minutes = 15)

            # Convert back to string
            return offset_dt.strftime("%Y-%m-%d %H:%M:%S")
        
        def map_pme_names(names_path, name_to_homologate):
            with open(names_path, 'r') as file:
                related_names_dict = json.load(file)
            return related_names_dict[name_to_homologate]

        nm_df = self.nms_dfs[selected]

        df = nm_df[1]

        # Handle empty voltages
        if ((df['Voltage colum mean'].fillna(0) == 0).all()) or (df['Voltage colum mean'].isna().all()):
            try:
                self.empy_volt_found.append((nm_df[0], 'la columna "Voltage colum mean" no tiene valores diferentes de cero o nulo'))
                
                # Get dates for query
                sample_date = df['Local Time'][sample]
                sample_date = datetime.strptime(sample_date, "%d/%m/%Y %H:%M:%S")
                start_dt, end_dt = get_month_boundaries_from_datetime(sample_date)

                # formatting dates
                start_time = change_to_local_time(start_dt, True)
                end_time = change_to_local_time(end_dt)
                
                # Connection string (update with your details)
                conn_str = (
                    r'DRIVER={ODBC Driver 18 for SQL Server};'
                    r'SERVER=SERVER;'
                    r'DATABASE=DATABASE;'
                    r'UID=UID;'
                    r'PWD=PWD;'
                    r'Trusted_Connection=no;'  # Explicitly use SQL Authentication
                    r'Encrypt=yes;'  # Enable encryption for security
                    r'TrustServerCertificate=yes;'
                    r'Connection Timeout=30;'  # Increase timeout to 30 seconds
                )

                # Connect to the database
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()

                # Build SQL query
                # Escape single quotes in source and measurements
                source = map_pme_names(self.pme_names_path, nm_df[0])

                measurements = ['Average Voltage Line-to-Line Mean']

                source_escaped = source.replace("'", "''")
                measurements_escaped = [m.replace("'", "''") for m in measurements]
                measurements_str = ", ".join(f"'{m}'" for m in measurements_escaped)
                
                query = f"""
                SELECT 
                    dl.TimestampUTC AS Time,
                    s.Name AS Device,
                    q.Name AS Measurement,
                    dl.Value
                FROM 
                    DataLog2 dl
                INNER JOIN 
                    Source s ON dl.SourceID = s.ID
                INNER JOIN 
                    Quantity q ON dl.QuantityID = q.ID
                WHERE 
                    s.Name = '{source_escaped}'
                    --AND q.Name IN ({measurements_str})
                    AND dl.QuantityID IN (170)
                    AND dl.TimestampUTC BETWEEN '{start_time}' AND '{end_time}'
                ORDER BY 
                    dl.TimestampUTC
                """

                # Execute query and load into DataFrame
                df_extracted = pd.read_sql(query, conn)

                # Close connection
                cursor.close()
                conn.close()

                if df_extracted.empty:
                    return df_extracted
                
                print(f'\ndf columns: {df_extracted.columns}\n')

                # Convert Time to datetime
                df_extracted['Time'] = pd.to_datetime(df_extracted['Time'])

                # Adjust for 5-hour offset (subtract 5 hours to match local time)
                df_extracted['Time'] = df_extracted['Time'] - pd.Timedelta(hours=5)

                # Pivot the DataFrame: Time as index, Measurements as columns, Values as data
                df_pivoted = df_extracted.pivot(index='Time', columns='Measurement', values='Value').reset_index()

                df_pivoted = df_pivoted[:-1]

                print(f'✍️  These was the dataframe column extracted for {nm_df[0]} \n{df_pivoted}\n')

                df['Voltage colum mean'] = df_pivoted['Average Voltage Line-to-Line Mean']
            except Exception as e:
                print(f'‼️  There was an error when voltage of {nm_df[0]} was being fixed | {e}')
                return df
        return df

    def handle_vll_data_exception(self, selected):
        
        nm_df = self.nms_dfs[selected]

        df = nm_df[1]

        # Handle exceptions
        if nm_df[0] == 'exception_column1':
            df['Voltage colum mean'] = df['Voltage colum mean']*1.73

        if nm_df[0] == 'exception_column2':
            df['Voltage colum mean'] = df['Voltage colum mean']*5.19

        return df

    def treating_small_numbers(self, selected, threshold = .0001):
        nm_df = self.nms_dfs[selected]

        df = nm_df[1]

        if not df.empty:
            # Get the first row of the DataFrame
            first_row = df.iloc[0, 1:]

            # Filter columns where the first value is below the threshold
            small_number_columns = first_row[(first_row < threshold) & (first_row > 0)].index.tolist()

            if small_number_columns:
                df[small_number_columns] = df[small_number_columns].round(6)
        return df
    
    #--Complementary functions------------------------------------------------------------------------------------------
    def get_month(self):
        i = 0
        keep_error = True

        while keep_error:
            if i > 20:
                break
            try:
                sample_data = self.nms_dfs[i][1]
                date = sample_data['Local Time'].iloc[0]
                keep_error = False
            except:
                i += 1
                pass
        
        if keep_error == False:
            date = str(date)
            date_part = date.strip().split()[0]
            yyyy, mmm, dd = date_part.split('-')
            month_abbr = mmm.lower()

            months = [
                'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
                ]
            mapping_months = {f'0{i+1}' if i<9 else f'{i+1}' : month for i, month in enumerate(months)}
            
            month_got = mapping_months.get(month_abbr)
            if not month_got:
                    raise ValueError(f"Unknown month abbreviation: {month_abbr!r} in {date!r}")
            
            return f'{month_got} del {yyyy}'
        else:
            return 'no encontrado'

    #--Orchestration------------------------------------------------------------------------------------------
    def get_ops(self):      # Here the order of operations can be changed       # I didn't use the description yet
        operation_list = [
            [self.drop_empty_columns, 'Eliminar columnas',
            'Se requiere eliminar primer los vacíos para que no intervengan en las próximas operaciones'],
            
            [self.handle_special_similarity_columns, 'Tratar casos especiales',
            'Actualmente el único caso especial es la similitud entre VII avg mean y algunos nombres de columnas'],
            
            [self.keep_just_similars, 'Añadir columnas faltantes',
            'Hay columnas que se esperan que necesariamente estén en el excel, en caso no estén, se completan como columnas vacías'],
            
            [self.datatime_column_handler, 'Corregir nombre de columna de tiempo',
            'La columna de de tiempo no siempre viene con el mismo nombre, por lo que es reescrita'],
            
            [self.lowercase_k, 'Corregir mayúscula en K',
            'Corrige el nombre de las columnas que tienen como mayúscula la letra K'],
            
            [self.lowercase_i, 'Corregir mayúscula en I',
            'Corrige el nombre de las columnas que tienen como mayúscula la letra I'],
            
            [self.add_missing_columns, 'Añadir columnas faltantes',
            'Hay columnas que se esperan que necesariamente estén en el excel, en caso no estén, se completan como columnas vacías'],
            
            [self.handle_holes, 'Completar agujeros e hipos',
             'Llena tanto los hipos como los espacios con más de un registro faltante'],

            [self.order_columns, 'Ordenar columnas',
            'Ordenar las columnas esperadas'],

            [self.handle_vll_data_exception, 'Tratar con excepciones del voltaje',
            'Para la columna de voltaje existen algunas excepciones'],

            [self.treating_small_numbers, 'Tratar con números muy pequeños',
            'Algunas columnas tienen números tan pequeños que se muestran en notación decimal, hecho que se quiere evitar']
        ]

        if self.pme_access_enabled:
            operation_list.insert(
                -3,
                [self.handle_vll_data_missing, 'Corregir voltajes vacíos o nulos',
                'En algunas casos, el voltaje no viene completo, por lo que aquí se extrae del PME de forma automática']
            )

        return operation_list
    
    def process_data(self):
        # Getting data      ## Add a try-except to handle errores here
        self.convertion_from_excel_to_df()
        self.excel_to_df_completed.emit('👷‍♂️  Data cargada y lista para ser procesada')

        # Fill previous table
        self.initial_data_got.emit(self.nms_dfs) #

        self.data_amount_established.emit(len(self.nms_dfs))

        self.month_got.emit(self.get_month())

        # Principal calculation
        i=0
        for operation, op_name, description in self.get_ops():
            self.operation_started.emit(f'📋  {description}')
            procesed_nms_dfs = []

            for i, (df_name, df) in enumerate(self.nms_dfs):

                try:
                    procesed_nms_dfs.append((df_name, operation(i)))
                    self.data_processed.emit(f'    ✅  El documento {df_name} fue exitosamente procesado')
                
                except Exception as e:
                    self.error_ocurred.emit(f'    ‼️  Hubo un error en el documento {df_name} para la operación {op_name}. Posiblemente está vacío | {e}')
                    self.errors_found.append((op_name, df_name))
                    #TODO: Maybe fill the df with zeros here when needed
                    
                self.one_more_proccesed.emit(i)

            self.operation_done.emit(f'👷‍♂️  La operación {op_name} ha culminado\n\n')

            self.nms_dfs = procesed_nms_dfs

        self.final_data_ready.emit(self.nms_dfs) #

        self.ready_for_report.emit(self.errors_found, self.empy_volt_found, self.sneezes_found, self.hipos_found)

        # Saving data
        if os.path.isdir(self.current_ouput_path):
                os.startfile(self.current_ouput_path)
        else:
            print(f"The folder '{self.current_ouput_path}' does not exist.")

        self.convertion_from_df_to_excel()