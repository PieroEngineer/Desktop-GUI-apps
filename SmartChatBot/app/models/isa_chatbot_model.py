import os, re, ast, requests
import pandas as pd

from zipfile import ZipFile
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from PyQt6.QtCore import pyqtSignal, pyqtSlot

from utils.dates_handler import extract_month_year, merge_time_ranges_by_device

# from models.gemini_llm_model import GeminiLLMModel
#from models.gpt4all_llm_model import Gpt4allLLMModel
from models.azureai_llm_model import AzureaiLlmModel

class IsaChatBotModel(AzureaiLlmModel):    
    understanding_step = pyqtSignal(str) 
    finding_data_step = pyqtSignal(str)
    error_finding_data_found = pyqtSignal(str)
    interpreting_results = pyqtSignal(str)
    answer_ready = pyqtSignal(str)
    message_processing_finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.df_curr = pd.DataFrame()
        self.mensual_data_used = []
        self.last_human_message = ''

        self.downloaded_data_path = r'app\data\Contenido\Downloaded'
        self.parquet_data_folder_path = r'app\data\Contenido\InParquet'

        self.criteria_path = r'app\data\Criterios\criteriofinal.xlsm'
        self.current_cf = self.load_criteria_from_excel_()

    def update_last_message(self, new_message):
        self.last_human_message = new_message

    def load_criteria_from_excel_(self):
        try:
            cf = pd.read_excel(self.criteria_path, sheet_name = 'Resumen', engine="openpyxl")
            cf = cf[['Columns of criteria'] + [f'RESTRICCIÓN {i}' for i in range(1,16)]]

            return cf
        except Exception as e:
            print("❌ Failed to load Excel:", e)
            exit(1)

    def resume_criteria_of_a_device_(self, cf, device_name):
        def resume_clarification_of_a_device(cf, device_name):
            if cf['EQUIPO'].isin([device_name]).any():
                cf = cf[cf['EQUIPO'] == device_name].copy()
            else:
                return ' This equipment does not have registered criteria '
            
            cf.reset_index(inplace=True)
            
            cf['ACLARACIÓN'] = 'Su mejor escenario es ' + cf['MEJOR ESCENARIO'] + ' para ' + cf['DÍA RECOMENDADO'] + ', pero cabe resaltar que ' + cf['COMENTARIO'] + ' '

            clarification = cf['ACLARACIÓN'][0]

            return clarification
        
        def resume_restrictions_of_a_device(cf, device_name):
            if cf['EQUIPO'].isin([device_name]).any():
                cf = cf[cf['EQUIPO'] == device_name].copy()
            else:
                return ' This equipment does not have registered criteria '
            
            cf.reset_index(inplace=True)
            cf = cf.fillna('')

            cf['RESTRICCIONES'] = ' La desconexión del equipo no puede cruzarse con los siguiente equipos: ' + cf[f'RESTRICCIÓN {1}']
            for i in range(2, 16):
                if cf[f'RESTRICCIÓN {i}'][0]:
                    cf['RESTRICCIONES'] = cf['RESTRICCIONES'] + ', ' + cf[f'RESTRICCIÓN {i}']

            restriction = cf['RESTRICCIONES'][0]

            if restriction == ' La desconexión del equipo no puede cruzarse con los siguiente equipos: ':
                restriction = f'No hay equipos con los que {device_name} no deba cruzarse'

            return restriction.strip()

        clarification = resume_clarification_of_a_device(cf, device_name)
        restriction = resume_restrictions_of_a_device(cf, device_name)

        return clarification + 'and ' + restriction
    

    def get_data_from_coes_(self, month_i, year, freq = 'Mensual'):
        months = [
        "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
        "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
        ]
                                                                                     
        def download_zip_from_url_(month_i, month, year, frequency, save_directory, filename = None):
            """
            Downloads a ZIP file from a given URL and saves it to a specified path.

            Parameters:
                url (str): The URL pointing directly to the ZIP file.
                filename (str): The name to save the ZIP file as (should include .zip).
                save_directory (str): The directory path where the ZIP file will be saved.

            Returns:
                str: The full path to the saved ZIP file.

            Raises:
                Exception: If the download fails or the status code is not 200.
            """

            url = fr"https://www.coes.org.pe/portal/browser/download?url=Operaci%C3%B3n%2FPrograma%20de%20Mantenimiento%2FPrograma%20{frequency}%2F{year}%2F{'0'+ f'{month_i+1}' if month_i < 9 else f'{month_i+1}'}_{month}%2FFinal%2FP{frequency.upper()}_{month}_{year}.zip"
            
            # Ensure the save directory exists
            os.makedirs(save_directory, exist_ok=True)
            
            # Build the full file path
            file_path = os.path.join(save_directory, filename)

            # Stream download for large files
            try:
                with requests.get(url, stream=True) as response:
                    response.raise_for_status()  # Raise an error for bad responses
                    with open(file_path, "wb") as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:  # Filter out keep-alive chunks
                                file.write(chunk)
                print(f"✅ File downloaded successfully: {file_path}\n")
                return file_path
            except Exception as e:
                raise Exception(f"Failed to download file: {e}")

        def get_df_from_coes_zip_(zip_path: str, inner_path: str) -> pd.DataFrame:
            """
            Extract an Excel (.xlsx) file from a ZIP and load it into a pandas DataFrame.

            Parameters
            ----------
            zip_path : str
                Path to the ZIP file.
            inner_path : str
                Relative path of the Excel file inside the ZIP (use forward slashes).
            sheet : str | int, default 0
                Sheet name or index to read.

            Returns
            -------
            pd.DataFrame
            """
            zip_path = Path(zip_path)
            if not zip_path.exists():
                raise FileNotFoundError(f"ZIP file not found: {zip_path}")
            print(f'Zip found ✅\n')
            with ZipFile(zip_path, "r") as zf:
                if inner_path not in zf.namelist():
                    raise FileNotFoundError(
                        f"'{inner_path}' not found in ZIP. Available files: {zf.namelist()}"
                    )
                print(f' Excel found in Zip✅\n')
                with zf.open(inner_path) as file:
                    return pd.read_excel(file, engine="openpyxl")

        file_name = f'{freq}_{months[month_i]}_{year}'
        #Xparquet_data_folder_path = r'data\Contenido\InParquet'

        #TODO: Here first verify in coes by date

        # Verify if data is in local
        file_path = os.path.join(self.parquet_data_folder_path, file_name+'.parquet')
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # If it's in local, use it
            print(f'🗃️  Data already in local for {file_name}\n')
            try:
                df = pd.read_parquet(self.parquet_data_folder_path + '\\' + file_name+'.parquet', engine="pyarrow")
            except Exception as e:
                print("❌ Failed to load parquet:", e)
        else:
            # If it isn't in local, download it and then concatenate it
            print(f'🔎  Data of {file_name} is not in local, so getting from COES\n')
            try:
                #Xdownloaded_data_path = r'data\Contenido\Downloaded'
                # Get zip from page
                download_zip_from_url_(month_i, months[month_i], year, freq, self.downloaded_data_path, file_name+'.zip')
                print(f'Data downloaded ✅ but verify if it is not empty 🧐\n')
                # Get dataframe from zip
                excel_relative_path = fr'Anexo1_Mantenimientos/Anexo1_Intervenciones_(Agentes)_{months[month_i]}_{year}.xlsm'
                df = get_df_from_coes_zip_(self.downloaded_data_path + '\\' + file_name+'.zip', excel_relative_path)
                print(f'Data found from zip ✅\n')
                # Process pandas
                df = df.iloc[7:, 1:17].reset_index(drop = True)
                df.columns = df.iloc[0, :]
                df = df.drop(0)
                df = df[['INICIO', 'FINAL', 'Dispon', 'EQUIPO']]

                df = df[df['Dispon'] == 'F/S']      ## Mod without E/S

                # Save in local as parquet
                df.to_parquet(self.parquet_data_folder_path + '\\' + file_name+'.parquet', engine="pyarrow", compression="snappy", index=False)
                print(f'Converted in parquet ✅\n')
            except Exception as e:
                print("❌ Failed to load data: ", e)
                exit(1)
                return pd.DataFrame()
        return df

    def find_data_(self, bot_answer):
        '''
        Receives:
        Set of tools to use

        Returns:
        list of answers collected
        '''

        self.answer_understood = self.understand_answer_(bot_answer)

        requested_tools = tuple(self.answer_understood.keys())

        intro = lambda function, answer: f'{function} got: {answer}'

        answer_accumulated = ''

        for requested_tool in requested_tools:
            tool_contribution = ''
            match requested_tool:
                # Available tools

                case 'get_new_mensual_data_required':   ## The chat bot has to give the first days of those months and years that the 
                    print(f'📚 Get mensual data requested by user\n')
                    involved_dates = self.answer_understood[requested_tool][1]
                    
                    self.get_mensual_data_(involved_dates)

                case 'select_only_decommissioned_devices':  #X Aparently deprecate
                    print(f'🔒  Only use decommissioned devices has been requested \n')
                    self.df_curr = self.df_curr[self.df_curr['Dispon'] == 'F/S']

                case 'select_any_devices':
                    print(f'🔓  Only use decommissioned devices has been requested \n')
                    self.df_curr = self.df_curr.copy()

                case 'get_dates_by_device_name':
                    print(f'📅  get dates by device name applied\n')
                    involved_devices = self.answer_understood[requested_tool][0]

                    for involved_device in involved_devices:
                        results = merge_time_ranges_by_device(self.df_curr, involved_device)
                        
                        for result in results:
                            tool_contribution += f"{involved_device} has (from {result[0]} to {result[1]}); "
                    ##print(f'\nResults:\n{results}')

                case 'get_complete_criteria_of_a_device':
                    print(f'🪧  show clarification of the equipment\n')
                    involved_devices = self.answer_understood[requested_tool][0]
                    for involved_device in involved_devices:
                        results = self.resume_criteria_of_a_device_(self.current_cf, involved_device)

                        tool_contribution += results + '; '

                #FIXME
                case 'get_clarification_clarification':
                    ''

                case 'get_restriction_clarification':
                    ''

                case _:
                    print(f'‼️ Called function was not found\n')
                    tool_contribution = f'{requested_tool} was not found '
            answer_accumulated += intro(requested_tool, tool_contribution)

        #Xself.tool_used.emit(answer_accumulated)
        return answer_accumulated
    
    def understand_answer_(self, bot_answer: str) -> dict:
        """
        Convert a string representing a Python dictionary into a real dictionary.

        Each value in the dictionary is expected to be a tuple of 3 lists:
            (list_of_strings, list_of_date_strings, list_of_strings)

        The function converts the date strings (format "%d/%m/%Y %H:%M")
        in the second list to datetime objects.

        Parameters:
            bot_answer (str): The input string representing a Python dictionary.

        Returns:
            dict: The parsed dictionary with datetime objects.
        """

        # Find all content within curly braces
        matches = re.findall(r'\{.*?\}', bot_answer)
        # Join the matched content to form the new string
        bot_answer =  "".join(matches)

        lines = bot_answer.splitlines()
        bot_answer = "".join(lines)

        # Safely evaluate the dictionary string
        try:
            parsed_dict = ast.literal_eval(bot_answer)
        except Exception as e:
            raise ValueError(f"Invalid dictionary string | {e}")

        tool_dict = {}

        for tool_name, value in parsed_dict.items():
            try:

                devices, dates, columns = value

                # Convert date strings to datetime objects
                converted_dates = []
                for d in dates:
                    try:
                        converted_dates.append(datetime.strptime(d, "%d/%m/%Y %H:%M"))
                    except Exception:
                        # If invalid or empty, skip or handle gracefully
                        pass

                if converted_dates:
                    self.get_mensual_data_(converted_dates)

                
                print(f'🗜️  For tool {tool_name}\n')
                print(f'        devices before assuming {devices}\n')
                devices = self.assume_name_(devices, tool_name)
                print(f'        devices after assuming {devices}\n')

                tool_dict[tool_name] = (devices, converted_dates, columns)
            except Exception as e:
                print(f"There was an error tool_name entry: {tool_name}  |  Error: {str(e)}\n")
                continue

        print(f'Interpreted dictionary:\n{tool_dict}\n')

        return tool_dict
    
    def get_mensual_data_(self, involved_dates):
        for involved_date in involved_dates:
            month_i, year = extract_month_year(involved_date)
            
            if not (month_i, year) in self.mensual_data_used:
                try:
                    df_extracted = self.get_data_from_coes_(month_i, year)
                except:
                    print(f'⚠️  First extracted data is not available in COES for month {month_i+1} of {year}, searching the previous month ({month_i})\n')
                    df_extracted = self.get_data_from_coes_(month_i-1, year)
                    month_i -= 1
                
                print(f'df_extracted\n{df_extracted}\n')
                if df_extracted.empty:
                    print(f'⚠️ When data of {month_i} {year} was called, it arrived empty\n')

                self.df_curr = pd.concat([self.df_curr, df_extracted], axis = 0, ignore_index = True)
                self.mensual_data_used.append((month_i, year))

    def assume_name_(self, input_list, tool_name, threshold = .8):

        def count_numeric_char(input_string):
            numeric_count = 0
            for char in input_string:
                if char.isdigit():
                    numeric_count += 1
            return numeric_count

        data_managing_tools = ['get_dates_by_device_name', 'get_new_mensual_data_required']
        criteria_tools = ['get_complete_criteria_of_a_device', 'get_clarification_clarification', 'get_restriction_clarification']

        if tool_name in data_managing_tools:
            reference_list = list(self.df_curr['EQUIPO'].unique())

        elif tool_name in criteria_tools:
            reference_list = list(self.current_cf['EQUIPO'].unique())

        match_list = []

        for input_elem in input_list:
            if ' ' in input_elem:
                # Take the word with more numbers
                words_in_code = input_elem.split()
                count_num_list = list(map(count_numeric_char, words_in_code))
                input_part_selected = words_in_code[count_num_list.index(max(count_num_list))]
            else:
                input_part_selected = input_elem

            for reference in reference_list:
                if input_part_selected in reference:
                    match_list.append(reference)
        match_list = list(set(match_list))

        if not match_list:

            def get_matches(target):
                matches = []

                for ref in reference_list:
                    score = SequenceMatcher(None, target, ref).ratio()
                    if score >= threshold:
                        matches.append(ref)
                return matches
            
            match_list = [get_matches(code) for code in input_list]
            match_list = list(set(item for sublist in match_list for item in sublist))
        return match_list
    

    
    @pyqtSlot()
    def handle_message(self):   # Main method
        print(f'🧑  ➡️  🤖:\n{self.last_human_message}\n')
        
        self.understanding_step.emit('🤖🔎  Estoy entendiendo tu mensaje')
        first_bot_response = self.interpret_prompt('Human prompt: ' + self.last_human_message)

        print(f'🤖  ➡️  🛠️:\n{first_bot_response}\n')
        
        self.finding_data_step.emit('🤖🗃️  Estoy encontrando los datos necesarios')
        try:
            algorithm_prompt = self.find_data_(first_bot_response)
        except Exception as e:
            print(f'🤕  There was an error when the bot tried to use a tool   |   {e}')
            self.error_finding_data_found.emit('🤖‼️  Hubo un problema cuando estuve procesando los datos')
            return "There was an error when the data was being processed"

        print(f'🛠️  ➡️  🤖:\n{'Pro algorithm prompt: ' + algorithm_prompt}\n')

        self.interpreting_results.emit('🤖🤞  Estoy interpretando los resultados obtenidos')
        last_bot_response = self.interpret_prompt('Pro algorithm prompt: ' + algorithm_prompt)   ## Maybe this will need self.last_human_message as input

        standardize_prompt = {
            "role": "user",
            "content": self.last_human_message
        }

        standardize_bot_response = {
            "role": "assistant",
            "content": last_bot_response,
        }

        self.last_interaction = [standardize_prompt, standardize_bot_response]

        print(f'🤖  ➡️  🧑:\n{last_bot_response}\n')

        self.answer_ready.emit(last_bot_response)
        #Xreturn last_bot_response

        self.message_processing_finished.emit()