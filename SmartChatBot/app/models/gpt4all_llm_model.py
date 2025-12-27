from gpt4all import GPT4All
from datetime import datetime
from PyQt6.QtCore import QObject


class Gpt4allLLMModel(QObject):
    """
    Local LLM using GPT4All (Phi-2.Q4_K_S.gguf)
    Replacement for GeminiLLMModel — same structure & method behavior.
    """

    def __init__(self):
        super().__init__()

        # Create a timestamped session
        current_datetime = datetime.now()

        # Permanent instruction (system message)
        dict_structre = '{tool_name: ([devices], [dates], [columns])}'
        self.instruction = f"""
        instruction
        """


        # Initialize GPT4All model (Phi-2 quantized)
        # allow_download=False assumes you already have the model locally
        #self.model = GPT4All("phi-2.Q4_K_S.gguf", allow_download=False)
        self.model = GPT4All("Phi-3-mini-4k-instruct-q4.gguf", allow_download=False)

        # Initialize an empty conversation history (JSON format)
        self.chat_history = '[]'

    # -----------------------------
    # Chat history management
    # -----------------------------
    def update_current_history(self, history):
        self.chat_history = history

    # -----------------------------
    # Core interaction
    # -----------------------------
    def interpret_prompt(self, prompt):
        """
        Respond to a user prompt, similar to Gemini's behavior.
        Includes permanent instruction + conversation history.
        """
        testing_offline = False  # For debugging fallback behavior

        if testing_offline:
            # Mock output for offline debugging
            return '{"get_new_mensual_data_required": ([], ["01/11/2025 00:00"], []), "get_complete_criteria_of_a_device": (["celda 6664"], [], [])}'

        if not prompt:
            print('\n🔎  You did not write some prompt for the chat bot\n')
            return None

        # Combine system instruction + last few messages
    
        history_list = self.chat_history

        full_prompt = (
            self.instruction.strip()
            + "\n\n"
            + prompt
            + "\n\n And the current human history prompts are the following:\n"
            + history_list
        )
        print(f'📋  The full prompt is \n{full_prompt}\n')

        # Generate response locally
        response_text = self.model.generate(
            full_prompt,
            max_tokens=150#X,
            #Xtemp=0.7
        ).strip()
        print(f'\n🤖🔗  AI technology reached with GPT4ALL\n')

        return response_text
