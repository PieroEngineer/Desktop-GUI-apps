from PyQt6.QtCore import QObject, QThread, pyqtSlot

##from app.models.record_model import RecordModel
from models.isa_chatbot_model import IsaChatBotModel
from models.history_model import HistoryModel

from views.main_window import MainWindow

class ChatbotController(QObject):
    def __init__(self, main_view: MainWindow):
        super().__init__()

        self.main_view = main_view

        self.main_view.send_button.clicked.connect(self.start_message_processing)
        self.main_view.input_field.returnPressed.connect(self.on_enter_key)

        self.is_running = False

        ##self.record_model = RecordModel()
        self.history_model = HistoryModel()

    #-------- Message sending --------
    def start_message_processing(self):
        if self.main_view.input_field.text() != '' and not self.is_running:
            self.is_running = True

            human_messsage_sent = self.main_view.input_field.text()
            
            self.isa_chatbot_model = IsaChatBotModel()      # Worker

            # Preparing the chatbot to receive the message history
            history = self.history_model.read_history()
            
            self.isa_chatbot_model.inject_current_history(history)
            
            # First actions in main view
            self.main_view.send_button.setEnabled(False)
            self.main_view.add_message(human_messsage_sent)
            self.main_view.input_field.clear()

            # Loading the human prompt in chatobot 
            self.isa_chatbot_model.update_last_message(human_messsage_sent)

            # Setting thread
            self.mssg_thread = QThread()
            self.isa_chatbot_model.moveToThread(self.mssg_thread)

            # Signals reactions
            self.mssg_thread.started.connect(self.isa_chatbot_model.handle_message)

            self.isa_chatbot_model.understanding_step.connect(self.on_update_process_state)
            self.isa_chatbot_model.finding_data_step.connect(self.on_update_process_state)
            self.isa_chatbot_model.error_finding_data_found.connect(self.on_update_process_state)
            self.isa_chatbot_model.interpreting_results.connect(self.on_update_process_state)
            self.isa_chatbot_model.answer_ready.connect(self.on_message_ready)

            # Finishg threads
            self.isa_chatbot_model.message_processing_finished.connect(self.mssg_thread.quit)
            self.isa_chatbot_model.message_processing_finished.connect(self.isa_chatbot_model.deleteLater)
            self.mssg_thread.finished.connect(self.mssg_thread.deleteLater)

            # Starting the thread
            self.mssg_thread.start()

    @pyqtSlot(str)
    def on_update_process_state(self, mssg):
        print(f'👷‍♂️👷‍♂️  mssg:  {mssg}\n')
        self.main_view.bot_info_label.start_new_process(mssg)
        self.main_view.bot_info_label.setText(mssg)

    @pyqtSlot(str)
    def on_message_ready(self, final_mssg):
        self.is_running = False
        self.main_view.add_message(final_mssg, False)
        self.main_view.bot_info_label.stop_last_process()
        self.main_view.send_button.setEnabled(True)

        last_interaction = self.isa_chatbot_model.get_last_interaction()
        self.history_model.add_in_history(last_interaction)

    def on_enter_key(self):
        if not self.is_running:
            self.start_message_processing()

    #-------- Message sending --------
    def start_recording_message(self):
        ''