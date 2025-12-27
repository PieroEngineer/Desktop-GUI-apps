from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QSizePolicy, QScrollArea
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize

from utils.handle_texts import bold_text

from views.additions.bot_info_view import BotInfoLoader

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ISA CHAT BOT 💙")
        self.setMinimumSize(500, 700)

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # Top Logo
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setPixmap(QPixmap(r"app\resources\images\Logo_ISA.png").scaled(259, 120, Qt.AspectRatioMode.KeepAspectRatio))
        self.main_layout.addWidget(self.logo_label)

        # Top info chat
        self.bot_info_label = BotInfoLoader()
        self.bot_info_label.setText('😁 Bienvenidos!! Soy el robot de ISA y estoy listo para ayudarte')
        self.bot_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bot_info_label.setObjectName("botInfoText")
        self.main_layout.addWidget(self.bot_info_label)

        # Chat Area (Scrollable)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setObjectName("chatArea")
        self.chat_layout = QVBoxLayout(scroll_content)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_area.setWidget(scroll_content)
        self.main_layout.addWidget(scroll_area)

        # Bottom Input Bar
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)

        # Mic button
        self.audio_button = QPushButton()
        self.audio_button.setIcon(QIcon(r'app\resources\icons\send_audio_icon.png'))
        self.audio_button.setIconSize(QSize(24, 24))
        self.audio_button.setObjectName("audioButton")
        input_layout.addWidget(self.audio_button)

        # Text input
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Escribe tu mensaje...")
        self.input_field.setObjectName("inputField")
        input_layout.addWidget(self.input_field, 1)

        # Send button
        self.send_button = QPushButton()
        self.send_button.setIcon(QIcon(r'app\resources\icons\send_message_icon.png'))
        self.send_button.setIconSize(QSize(24, 24))
        self.send_button.setObjectName("sendButton")
        input_layout.addWidget(self.send_button)

        self.main_layout.addLayout(input_layout)

        # Apply Style
        self.setStyleSheet(self.load_styles())

    # Message Handling
    def add_message(self, text, is_user=True):      ## Future improvement (Convert the text block in a class)
        """Add a chat bubble with animation."""
        bubble = QLabel(bold_text(text))
        bubble.setTextFormat(Qt.TextFormat.RichText) # Enable rich text formatting
        bubble.setWordWrap(True)
        bubble.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Styling for user/bot bubbles
        if is_user:
            bubble.setStyleSheet("background:#FE5000; color:white; padding:8px; border-radius:10px;")
            bubble.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            bubble.setStyleSheet("background:#FFFFFF; color:black; padding:8px; border-radius:10px;")
            bubble.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.chat_layout.addWidget(bubble)

        ## Open the possibility to convert "bubble" variable and edit it (with three points maybe)

    def load_styles(self):
        """Returns QSS styles for a modern rounded look."""
        return """
        QWidget {
            background-color: #FFFFFF;
            font-family: Segoe UI, sans-serif;
            font-size: 14px;
            color: #ECEFF4;
        }

        QLabel {
            border: none;
        }

        QLabel#botInfoText {
            border: none;
            color: blue;
        }

        #chatArea {
            background-color: #EAF3FF;
            border-radius: 12px;
            padding: 8px;
            color: #ECEFF4;
        }

        #inputField {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 6px 10px;
            border: 1px solid #4C566A;
            color: black;
        }

        #inputField:focus {
            border: 1px solid #88C0D0;
            background-color: #EAF3FF;
        }

        QPushButton {
            background-color: #5E81AC;
            border-radius: 9px;
            padding: 8px 14px;
            color: white;
        }

        QPushButton:hover {
            background-color: #EAF3FF;
        }

        QPushButton#sendButton {
            background-color: #0077CC;
        }

        QPushButton#sendButton:hover {
            background-color: #00378F;
        }

        QPushButton#audioButton {
            background-color: #FFFFFF;
        }

        QPushButton#audioButton:hover {
            background-color: #EAF3FF;
        }
        """