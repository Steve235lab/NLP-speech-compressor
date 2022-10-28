from PyQt5.QtWidgets import QPushButton

from app_core import APP_CORE


class CompressButton(QPushButton):
    def __init__(self, parent=None):
        super(QPushButton, self).__init__(parent)
        self.setStyleSheet("QPushButton{border-image: url(../res/SlideWindow.png)}"
                           "QPushButton:hover{border-image: url(../res/SlideWindow_hover.png)}"
                           "QPushButton:pressed{border-image: url(../res/SlideWindow.png}")
        self.clicked.connect(self.compress)

    def compress(self):
        APP_CORE.compress()
