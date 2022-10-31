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
        self.setToolTip('开始讲话')

    def switch(self):
        if APP_CORE.is_recording is False:  # 没在录音
            APP_CORE.start_input_audio()
            self.setStyleSheet("QPushButton{border-image: url(../res/mic_recording.png)}"
                               "QPushButton:hover{border-image: url(../res/mic_recording_hover.png)}"
                               "QPushButton:pressed{border-image: url(../res/mic.png}")
            self.setToolTip('停止讲话')
        else:   # 在录音
            APP_CORE.stop_input_audio()
            self.setStyleSheet("QPushButton{border-image: url(../res/mic.png)}"
                               "QPushButton:hover{border-image: url(../res/mic_hover.png)}"
                               "QPushButton:pressed{border-image: url(../res/mic_recording.png}")
            self.setToolTip('开始讲话')
