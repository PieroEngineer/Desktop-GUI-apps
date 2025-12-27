
import random
#from typing import Dict, Tuple, Optional, List

from PyQt6.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class LineScrollWidget(QScrollArea):
    """
    A scrollable widget that manages elements with:
    - Name label
    - Color square
    - Optional 'Nom.' button
    - 'X' button for removal

    Attributes:
        elements_dict: Dict[str, Tuple[Tuple[int,int,int], Optional[QPushButton], QPushButton]]
        available_colors: List[Tuple[int,int,int]]
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Container widget inside scroll
        self.container = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setWidget(self.container)
        self.setWidgetResizable(True)

        # Data structures
        self.elements_dict = {}
        self.available_colors= [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 165, 0), (128, 0, 128), (0, 255, 255),
            (255, 192, 203), (128, 128, 128)
        ]

    def add_element(self, name: str, include_nom: int, color: str, should_include_nom: str):#X|-> , fix_red: bool = False):
        """Add a new element with a random color and optional 'Nom.' button."""
        if name in self.elements_dict:
            raise ValueError(f"Element '{name}' already exists.")

        # Create element widget
        element_widget = QWidget()
        h_layout = QHBoxLayout(element_widget)
        h_layout.setContentsMargins(5, 5, 5, 5)

        # Color square
        color_label = QLabel()
        color_label.setFixedSize(20, 20)
        color_label.setStyleSheet(f"background-color: {color};")

        # Name label
        name_label = QLabel(name)

        # 'Nom.' button
        nom_button = QPushButton("Nom.") if include_nom else None

        # Remove button
        remove_button = QPushButton("✖️")
        remove_button.setFixedWidth(30)

        # Add widgets to layout
        h_layout.addWidget(color_label)
        h_layout.addWidget(name_label)
        if nom_button:
            h_layout.addWidget(nom_button)
        elif should_include_nom:
            h_layout.addWidget(QLabel('⚠️ Sin Nom.'))
        h_layout.addWidget(remove_button)

        # Add to scroll layout
        self.layout.addWidget(element_widget)

        # Store in dictionary
        self.elements_dict[name] = (color, nom_button, remove_button)

    def remove_element(self, name: str):
        """Remove an element by name from the scroll and dictionary."""
        if name not in self.elements_dict:
            return

        # Find widget in layout
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    # Check if this widget contains the name label
                    for j in range(widget.layout().count()):
                        sub_item = widget.layout().itemAt(j)
                        sub_widget = sub_item.widget()
                        if isinstance(sub_widget, QLabel) and sub_widget.text() == name:
                            # Remove widget from layout and delete
                            self.layout.removeWidget(widget)
                            widget.deleteLater()
                            break

        # Remove from dictionary
        del self.elements_dict[name]
