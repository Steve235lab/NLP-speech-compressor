# Qt_SwitchButton.py
# 自定义控件类


from PyQt5.QtWidgets import QPushButton

from app_core import APP_CORE


class SwitchButton(QPushButton):
    def __init__(self, parent=None):
        super(QPushButton, self).__init__(parent)
        self.setStyleSheet("QPushButton{border-image: url(../res/mic.png)}"
                           "QPushButton:hover{border-image: url(../res/mic_hover.png)}"
                           "QPushButton:pressed{border-image: url(../res/mic_recording.png}")
        self.clicked.connect(self.switch)

    def switch(self):
        if APP_CORE.is_recording is False:
            APP_CORE.start_input_audio()
            self.setStyleSheet("QPushButton{border-image: url(../res/mic_recording.png)}"
                               "QPushButton:hover{border-image: url(../res/mic_recording_hover.png)}"
                               "QPushButton:pressed{border-image: url(../res/mic.png}")
        else:
            APP_CORE.stop_input_audio()
            self.setStyleSheet("QPushButton{border-image: url(../res/mic.png)}"
                               "QPushButton:hover{border-image: url(../res/mic_hover.png)}"
                               "QPushButton:pressed{border-image: url(../res/mic_recording.png}")
