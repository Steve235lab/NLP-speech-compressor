from PyQt5 import QtCore
from PyQt5.QtWidgets import QTextEdit

from app_core import APP_CORE


class OriginalText(QTextEdit):
    def __init__(self, parent=None):
        super(QTextEdit, self).__init__(parent)
        self.setReadOnly(True)
        self.update_value()

    def update_value(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.set_text)
        timer.start(100)

    def set_text(self):
        self.setText(APP_CORE.get_original_text())
