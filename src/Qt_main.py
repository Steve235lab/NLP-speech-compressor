from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

# 以下引用方便打包
import api_info
import app_core
import compressor
import local_audio_input
import local_main
import process_result_dict
import Qt_CompressButton
import Qt_CompressedText
import Qt_OriginalText
import Qt_SwitchButton
import rank_bm25
import rtasr_client
import speech2text


# 建立图形窗口
Form, Window = uic.loadUiType("main_window.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec_()

