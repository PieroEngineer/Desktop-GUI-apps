import base64
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

from app.resources.logo_encoded import LOGO_IMAGE

class AboutWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information")
        self.setModal(False)  # non-modal
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        self.encoded_image = LOGO_IMAGE
        self.text = """
                <h1>GUI - MANTENIMIENTO</h1>

                <h3>VERSIÓN 1.0.0</h3>
                <p>Coordinación de Sistema de potencia</p>
                <p>Subgerencia de operaciones</p>

                <p><b>Copyright © 2025 Red de energía del Perú S.A.</b></p>
            """

        # ---- Left: Image ----
        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        pix: QPixmap = self._pixmap_from_encoded_image()
        if not pix.isNull():
            pix = pix.scaledToWidth(160, Qt.TransformationMode.SmoothTransformation)
            self.img_label.setPixmap(pix)
        else:
            self.img_label.setText("Image\nnot available")
            self.img_label.setStyleSheet("color:#a00;")

        # ---- Right: Text ----
        self.text_label = QLabel(self.text)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # ---- Top Row ----
        self.top_row = QHBoxLayout()
        self.top_row.addWidget(self.img_label)
        self.top_row.addSpacing(12)
        self.top_row.addWidget(self.text_label, stretch=1)

        # ---- Bottom: Accept Button ----
        self.accept_btn = QPushButton("Accept")
        
        # ---- Main Layout ----
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.top_row)
        self.main_layout.addSpacing(12)
        self.main_layout.addWidget(self.accept_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.setMinimumWidth(420)

    def _pixmap_from_encoded_image(self) -> QPixmap:
        """
        encoded_image can be:
        - A file path to an image, or
        - A base64 string (raw), or
        - A data URL: 'data:image/png;base64,AAAA...'
        Returns a QPixmap (may be null if load fails).
        """
        pix = QPixmap()

        if not self.encoded_image:
            return pix

        # Heuristics to detect data URL or base64
        is_data_url = self.encoded_image.strip().lower().startswith("data:image/")
        looks_like_b64 = not is_data_url and all(c.isalnum() or c in "+/=\n\r" for c in self.encoded_image.strip())

        try:
            if is_data_url:
                # Format: data:image/png;base64,AAAA...
                header, b64data = self.encoded_image.split(",", 1)
                raw = base64.b64decode(b64data)
                pix.loadFromData(raw)
            elif looks_like_b64:
                raw = base64.b64decode(self.encoded_image)
                pix.loadFromData(raw)
            else:
                # Treat as file path
                pix.load(self.encoded_image)
        except Exception:
            # leave pix as null if anything fails
            pass

        return pix
    
    