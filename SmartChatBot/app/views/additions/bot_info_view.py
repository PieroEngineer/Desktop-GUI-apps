from PyQt6.QtWidgets import QLabel

from PyQt6.QtCore import QTimer

class BotInfoLoader(QLabel):
    def __init__(self, parent=None):
        super().__init__("😁 Bienvenid@s!! Soy el robot de ISA y estoy listo para ayudarte", parent)
        self.timer = QTimer(self)

    def start_new_process(self, current_text):
        if not self.timer.isActive():
            self.dot_count = 0
            self.timer.timeout.connect(lambda: self.update_point_state(current_text))
            self.timer.start(500)
            self.setStyleSheet("color: blue; font-style: italic; padding:5px;")

    def update_point_state(self, process_text):
        self.dot_count = (self.dot_count + 1) % 4
        self.setText(process_text + "." * self.dot_count)

    def stop_last_process(self):
        if self.timer.isActive():
            self.timer.stop()
            self.setText('😁 Bienvenid@s!! Soy el robot de ISA y estoy listo para ayudarte')