# Qt_CompressButton.py
# 自定义控件类


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton

from app_core import APP_CORE


class CompressButton(QPushButton):
    def __init__(self, parent=None):
        super(CompressButton, self).__init__(parent)
        self.setStyleSheet("QPushButton{border-image: url(../res/SlideWindow.png)}"
                           "QPushButton:hover{border-image: url(../res/SlideWindow_hover.png)}"
                           "QPushButton:pressed{border-image: url(../res/SlideWindow.png}")
        self.clicked.connect(self.compress)
        self.parent = parent

    def compress(self):
        original_text_obj = self.parent.findChild(QtWidgets.QTextEdit, "original_text")
        APP_CORE.compressor.original_text = original_text_obj.toPlainText()
        print(APP_CORE.compressor.original_text)
        APP_CORE.compress()
