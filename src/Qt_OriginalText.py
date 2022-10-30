# Qt_OriginalText.py
# 自定义控件类


from PyQt5 import QtCore
from PyQt5.QtWidgets import QTextEdit

from app_core import APP_CORE


class OriginalText(QTextEdit):
    def __init__(self, parent=None):
        super(OriginalText, self).__init__(parent)
        self.setReadOnly(False)
        self.setText(APP_CORE.get_original_text())
        self.update_value()

    def update_value(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.set_text)
        timer.start(100)

    def set_text(self):
        if APP_CORE.is_recording is True:
            self.setText(APP_CORE.get_original_text())
