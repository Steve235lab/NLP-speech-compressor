from threading import Thread
import time

from rtasr_client import Client
from api_info import app_id, api_key
from local_audio_input import LocalAudio


class Speech2Text:
    def __init__(self):
        self.rtasr_client = Client(app_id, api_key)
        self.local_audio = LocalAudio()
        self.frame_index = 0
        self.input_send_thread = Thread(target=self.input_audio_and_send)

    def input_audio_and_send(self):
        audio_input_thread = Thread(target=self.local_audio.start)
        audio_input_thread.start()
        time.sleep(1)
        while self.local_audio.is_recording is True or self.frame_index < len(self.local_audio.frames) - 1:
            try:
                self.rtasr_client.send(self.local_audio.frames[self.frame_index])
                # print(self.frame_index)
                self.frame_index += 1
            except:
                pass

    def start(self):
        self.input_send_thread.start()

    def cut(self):
        self.local_audio.cut()
        self.rtasr_client.send_end_tag()


if __name__ == '__main__':
    s2t = Speech2Text()
    s2t.start()
    time.sleep(5)
    s2t.cut()

