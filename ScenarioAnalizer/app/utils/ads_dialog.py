
from PyQt6.QtWidgets import QMessageBox

def show_ads(commentary: str):
    msg = QMessageBox()
    msg.setWindowTitle("Advertisement")
    msg.setText(commentary)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()
