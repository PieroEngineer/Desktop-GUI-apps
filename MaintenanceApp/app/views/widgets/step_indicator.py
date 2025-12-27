from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QFont
from PyQt6.QtCore import Qt

class StepIndicator(QWidget):
    def __init__(self):
        super().__init__()
        self.steps = []
        self.completed_steps = 0
        self.setMinimumHeight(80)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.steps:
            step_width = self.width() // len(self.steps)
            radius = 20

            for i, step in enumerate(self.steps):
                center_x = step_width * i + step_width // 2
                center_y = 25

                # Draw connector line
                if i < len(self.steps) - 1:
                    painter.setPen(QPen(QColor("#000000"), 2))
                    painter.drawLine(center_x + radius, center_y, center_x + step_width - radius, center_y)

                # Draw circle
                if i < self.completed_steps:
                    painter.setBrush(QBrush(QColor("#4CAF50")))  # green for done
                    painter.setPen(Qt.PenStyle.NoPen)
                elif i == self.completed_steps:
                    painter.setBrush(QBrush(QColor("#FFA500")))  # Orange for charging
                    painter.setPen(Qt.PenStyle.NoPen)
                else:
                    painter.setBrush(QBrush(QColor("#CCCCCC")))  # gray for pending
                    painter.setPen(Qt.PenStyle.NoPen)

                painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

                # Step number or checkmark
                painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
                painter.setPen(Qt.GlobalColor.white)
                if i < self.completed_steps:
                    painter.drawText(center_x - 6, center_y + 5, "✔")
                elif i == self.completed_steps:
                    painter.drawText(center_x - 6, center_y + 5, "O")
                else:
                    painter.drawText(center_x - 5, center_y + 5, str(i+1))

                # Step label
                painter.setFont(QFont("Arial", 8))
                painter.setPen(QColor("#333333"))
                painter.drawText(center_x - 40, center_y + 4, 80, 80, Qt.AlignmentFlag.AlignCenter, step)
        else:
            """Draws a subtle rounded rectangle with centered placeholder text."""
            rect = self.rect().adjusted(8, 8, -8, -8)
            radius = 10

            # Frame
            pen = QPen(QColor("#999999"))
            pen.setStyle(Qt.PenStyle.DashLine)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(rect, radius, radius)

            # Text
            painter.setPen(QColor("#666666"))
            font = QFont(self.font())
            font.setPointSize(max(9, font.pointSize()))
            font.setBold(True)
            painter.setFont(font)

            painter.drawText(
                rect,
                Qt.AlignmentFlag.AlignCenter,
                "Empezar operación para ver el progreso"
            )

    def set_steps(self, current_stepts):
        self.steps = current_stepts

    def one_step_finished(self):
        self.completed_steps += 1
        if self.completed_steps > len(self.steps):
            self.completed_steps = len(self.steps)
        self.update()
    
    def reset_steps(self):
        self.completed_steps = 0
        self.update()
