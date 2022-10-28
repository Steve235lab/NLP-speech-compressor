from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


# 建立图形窗口
Form, Window = uic.loadUiType("main_window.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec_()

