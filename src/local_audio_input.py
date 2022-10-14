# local_audio_input.py
# 用于本地测试的语音输入功能模块


import pyaudio


class LocalAudio:
    def __init__(self):
        self.is_recording = False
        self.chunk_size = 1280
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.frames = []    # 音频帧列表

    def start(self):
        """启动音频录制

        :return: None
        """
        print('* recording')
        self.is_recording = True
        self.stream = self.pa.open(format=self.audio_format,
                                   channels=self.channels,
                                   rate=self.rate,
                                   input=True,
                                   frames_per_buffer=self.chunk_size)
        while self.is_recording is True:
            self.frames.append(self.stream.read(self.chunk_size))

    def cut(self):
        """终止音频录制

        :return: None
        """
        print('* done recording')
        self.is_recording = False
        try:
            self.stream.stop_stream()
            self.stream.close()
        except AttributeError:
            pass
        finally:
            pass
        self.pa.terminate()
