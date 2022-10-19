# speech2text.py
# 基于科大讯飞API的实时语音转文字功能模块


from threading import Thread
import time

from rtasr_client import Client
from api_info import app_id, api_key
from local_audio_input import LocalAudio


class Speech2Text:
    def __init__(self, output_words: bool = True):
        """

        :param output_words: True - 以完成分词后的形式将结果写入输出文件, False - 以整段连贯文字的方式将结果写入输出文件
        :return: None
        """
        self.rtasr_client = Client(app_id, api_key)
        self.local_audio = LocalAudio()
        self.frame_index = 0    # 语音输入与音频帧发送异步控制帧编号计数器
        self.input_send_thread = Thread(target=self.input_audio_and_send)   # 以附加线程的方式运行，便于中断
        self.output_words = output_words

    def input_audio_and_send(self):
        """音频输入与发送
        通过麦克风进行音频输入与将音频帧发送到API接口以多线程异步的方式进行

        :return: None
        """
        # 以附加线程的方式进行音频输入
        audio_input_thread = Thread(target=self.local_audio.start)
        audio_input_thread.start()
        time.sleep(0.5)
        # 当 音频输入未结束 或 已输入的音频帧未全部发送至API端口 时
        while self.local_audio.is_recording is True or self.frame_index < len(self.local_audio.frames) - 1:
            try:    # 尝试发送下一帧（如果有）
                self.rtasr_client.send(self.local_audio.frames[self.frame_index])
                # print(self.frame_index)
                self.frame_index += 1
            except:
                pass

    def start(self):
        """在附加线程中启动语音转文字功能

        :return: None
        """
        self.input_send_thread.start()

    def cut(self):
        """终止语音转文字
        * 终止音频输入
        * 向API端口发送结束标志
        * 等待结果接受完毕后将最终结果写入文件存档

        :return: None
        """
        # 终止音频输入
        self.local_audio.cut()
        time.sleep(0.5)
        # 向API端口发送结束标志
        self.rtasr_client.send_end_tag()
        time.sleep(0.5)
        # 以 speech2text_0123456789.txt 作为文件名对最终结果存档（仅用作中间结果分析，后续步骤直接访问内存对象，无需从该存档文件中加载数据）
        timestamp = str(int(time.time()))
        output_file = open('../output/speech2text/speech2text_' + timestamp + '.txt', 'w', encoding='utf-8')
        if self.output_words is False:
            output_file.write(self.rtasr_client.final_output)
        else:
            content = ''
            for word in self.rtasr_client.final_words:
                content += word + '\n'
            output_file.write(content)
        output_file.close()


if __name__ == '__main__':
    # 实例化
    s2t = Speech2Text(output_words=True)
    # 启动服务
    s2t.start()
    # 运行时长
    time.sleep(30)
    # 终止服务
    s2t.cut()

