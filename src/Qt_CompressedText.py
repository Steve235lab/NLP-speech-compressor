# Qt_CompressedText.py
# 自定义控件类


from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout
import pyperclip

from app_core import APP_CORE


class CopyButton(QPushButton):
    def __init__(self, parent=None):
        super(CopyButton, self).__init__(parent)
        self.parent = parent
        self.clicked.connect(self.copy)

    def copy(self):
        """将父类中的内容复制到剪贴板"""
        content = self.parent.toPlainText()
        pyperclip.copy(content)


class CompressedText(QTextEdit):
    def __init__(self, parent=None):
        super(QTextEdit, self).__init__(parent)
        self.setReadOnly(True)
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

    def update_value(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.set_text)
        timer.start(1000)

    def set_text(self):
        self.setText(APP_CORE.get_compressed_text())

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        # 光标指向时显示复制按钮
        self.copy_button.show()

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        # 光标移开时隐藏复制按钮
        self.copy_button.hide()
