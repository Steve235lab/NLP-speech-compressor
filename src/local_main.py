# local_main.py
# 适用于本地运行的应用程序入口


import time

from speech2text import Speech2Text
from compressor import Compressor


class LocalApp:
    def __init__(self):
        self.s2t = None
        self.compressor = Compressor('', [])
        self.is_recording = False

    def start_input_audio(self):
        self.s2t = Speech2Text()
        self.s2t.start()
        self.is_recording = True

    def stop_input_audio(self):
        if self.is_recording is True:
            self.s2t.cut()
        self.is_recording = False

    def get_original_text(self) -> str:
        if self.s2t is not None:
            return self.s2t.rtasr_client.final_output
        else:
            return "请先录入音频！"

    def get_original_words(self) -> list:
        if self.s2t is not None:
            return self.s2t.rtasr_client.final_words
        else:
            return "请先录入音频！"

    def get_compressed_text(self) -> str:
        if self.compressor is not None:
            return self.compressor.original_text
        else:
            return "请先执行压缩操作！"

    def compress(self):
        if len(self.compressor.original_text) > 0:
            print("正在对文本进行精简压缩...")
            start_time = time.time()
            self.compressor.compress()
            end_time = time.time()
            print("压缩已完成，用时：", end_time - start_time)
        else:
            print("未检测到已录入文本，请先录入文本！")


if __name__ == '__main__':
    my_app = LocalApp()
    while True:
        cmd = input(">>>")
        if cmd == 'start':
            my_app.start_input_audio()
        elif cmd == 'cut':
            my_app.stop_input_audio()
        elif cmd == 'compress':
            my_app.compress()
        elif cmd == 'print original text':
            print(my_app.get_original_text())
        elif cmd == 'print original words':
            print(my_app.get_original_words())
        elif cmd == 'print compressed text':
            print(my_app.get_compressed_text())
        elif cmd == 'is recording':
            print(my_app.is_recording)

