from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel


class LabelClickable(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
