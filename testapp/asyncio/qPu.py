import sys

from PyQt5.QtWidgets import *


class MyQpush(QPushButton):
    def __init__(self, label="wow", parent=None):
        super().__init__(label, parent)
        self.setStyleSheet("background-color: lightblue; font-size: 16px;")
        self.clicked.connect(self.on_click)

    def on_click(self):
        # Emit the custom signal when clicked
        print(f"{self.text()} was clicked!")
        # self.custom_signal.emit()

