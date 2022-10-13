import wave
import pyaudio
from api_demos.rtasr_python3_demo.python.rtasr_python3_demo import Client
from api_info import app_id, api_key


class Speech2Text:
    def __init__(self):
        self.rtasr_client = Client(app_id, api_key)


if __name__ == '__main__':
    s2t = Speech2Text()
    s2t.rtasr_client.send(r"api_demos/rtasr_python3_demo/python/test_1.pcm")

