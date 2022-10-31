# Qt_OriginalText.py
# 自定义控件类


from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QHBoxLayout

from app_core import APP_CORE
from Qt_CompressedText import CopyButton


class OriginalText(QTextEdit):
    def __init__(self, parent=None):
        super(OriginalText, self).__init__(parent)
        self.setReadOnly(False)
        self.setText(APP_CORE.get_original_text())
        self.update_value()
        self.copy_button = CopyButton(self)
        self.copy_button.setMaximumSize(QtCore.QSize(50, 50))
        self.copy_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.copy_button.setText("复制")
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.setFont(font)
        self.copy_button.hide()
        self.vLayout = QVBoxLayout()
        self.vLayout.setContentsMargins(0, 0, 15, 0)  # 设置Margin让按钮更加贴近右上角（滚动条会遮住按钮，所以有边缘设置15）
        self.vLayout.addWidget(self.copy_button)
        self.vLayout.addStretch(1)  # 添加拉升将按钮移动到右上角
        self.hLayout = QHBoxLayout()
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.addStretch(1)
        self.hLayout.addLayout(self.vLayout)
        self.setLayout(self.hLayout)
        self.setToolTip('原始文本')

    def update_value(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.set_text)
        timer.start(100)

    def set_text(self):
        if APP_CORE.is_recording is True:
            self.setText(APP_CORE.get_original_text())

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        # 光标指向时显示复制按钮
        self.copy_button.show()

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        # 光标移开时隐藏复制按钮
        self.copy_button.hide()
