import google.generativeai as genai

from PyQt6.QtCore import QObject

from datetime import datetime

from utils.keys import GEMINI_API_KEY

class GeminiLLMModel(QObject):

    def __init__(self):
        super().__init__()

        genai.configure(api_key=GEMINI_API_KEY)

        current_datetime = datetime.now()

        #Sometimes if the toolbox doesn't find the equipment, return similars, so take care with that.
        #select_only_decommissioned_devices: This tool should be always (important) called unless the human explicitly tells it otherwise. This tool has no parameters, this function just lets the other tools know that they have to work only with decommissioned devices for example

        self.instruction = f"""
        instruction
        """

        self.model = genai.GenerativeModel("gemini-2.5-flash", system_instruction = self.instruction)
        
        self.chat = self.model.start_chat(history=[])

        self.chat_history = '[]'


    def inject_current_history(self, history):
        self.chat_history = history

    def interpret_prompt(self, prompt):
        testing_offline = False  ## Just for testing
        if testing_offline:
            return '{"get_new_mensual_data_required": ([], ["01/11/2025 00:00"], []), "get_complete_criteria_of_a_device": (["celda 6664"], [], [])}'
        else:
            if not prompt:
                print('\n🔎  You did not write some prompt for the chat bot\n')
            else:
                if prompt.startswith('Human'):
                    prompt = prompt + '\n📃  Current conversation history is the following:\n' + self.chat_history

                response = self.chat.send_message(prompt)
                print(f'\n🤖🔗  AI technology reached with Gemini API\n')

                return response.text