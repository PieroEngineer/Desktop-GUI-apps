from openai import AzureOpenAI

from datetime import datetime

from PyQt6.QtCore import QObject

class AzureaiLlmModel(QObject):
    """
    Local LLM using GPT4All (Phi-2.Q4_K_S.gguf)
    Replacement for GeminiLLMModel — same structure & method behavior.
    """

    def __init__(self):
        super().__init__()

        self.endpoint = "endpoint"
        self.model_name = "model_name"    ## Unused
        self.deployment = "deployment"

        subscription_key = "subscription_keyW"
        api_version = "api_version"

        self.client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=self.endpoint,
            api_key=subscription_key,
        )

        # Create a timestamped session
        current_datetime = datetime.now()

        # Permanent instruction (system message)
        self.instruction = f"""
        instruction
        """

        self.last_interaction = []

    def get_last_interaction(self):
        return self.last_interaction

    # Chat history management
    def inject_current_history(self, history):
        self.history_injected = history

    # Core interaction
    def interpret_prompt(self, prompt: str):
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
            return ''

        standardize_instruction = {
            "role": "system",
            "content": self.instruction
        }

        standardize_prompt = {
            "role": "user",
            "content": prompt
        }
        
        ## System instruction + history + current human prompt
        full_prompt = [standardize_instruction] + self.history_injected + [standardize_prompt]
        print(f'📋  The full prompt (whithout instructions) is \n{full_prompt[1:]}\n')

        # Generate response 
        response = self.client.chat.completions.create(
            messages=full_prompt,
            max_completion_tokens =16384,
            model=self.deployment
        )
        print(f'\n🤖🔗  AI technology reached from Azure\n')

        return response.choices[0].message.content