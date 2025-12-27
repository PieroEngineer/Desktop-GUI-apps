import json

class HistoryModel:
    def __init__(self):
        self._clear_history()

    def add_in_history(self, new_history):
        with open(r'app\chat_history.json', 'r') as f:
            data: list = json.load(f)

        data += new_history

        with open(r'app\chat_history.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    def read_history(self):
        with open(r'app\chat_history.json', 'r') as f:
            data = json.load(f)
        return data

    def _clear_history(self):
        with open(r'app\chat_history.json', 'r') as f:
            data = json.load(f)

        data = []

        with open(r'app\chat_history.json', 'w') as f:
            json.dump(data, f, indent=4)

    ##
    # def limit_history(self, max_register = 20):
    #     if len(self.history) > max_register:
    #             self.history = [self.history[0]] + self.history[-(max_register-1):]