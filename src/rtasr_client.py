# rtasr_client.py
# 基于科大讯飞“实时语音转写” API demo 二次开发


import hashlib
import hmac
import base64
from socket import *
import json, time, threading
from websocket import create_connection
import websocket
from urllib.parse import quote
import logging
import os
from api_info import app_id, api_key
from process_result_dict import process_result_dict


# reload(sys)
# sys.setdefaultencoding("utf8")
class Client:
    def __init__(self, app_id, api_key):
        base_url = "ws://rtasr.xfyun.cn/v1/ws"
        ts = str(int(time.time()))
        tt = (app_id + ts).encode('utf-8')
        md5 = hashlib.md5()
        md5.update(tt)
        baseString = md5.hexdigest()
        baseString = bytes(baseString, encoding='utf-8')

        apiKey = api_key.encode('utf-8')
        signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        self.end_tag = "{\"end\": true}"

        self.ws = create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa))
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()
        self.result = None
        self.outputs = []   # 以字符串列表的形式保存每次API返回的结果
        # self.full_sentences = []
        # self.selected_ct = 0
        # self.recv_end_flag = False
        # self.select_thread = threading.Thread(target=self.select_full_sentence)
        # self.select_thread.start()
        self.final_output = ''  # 用来保存最终结果的字符串
        self.final_words = []

    def send(self, audio_frame):
        """向API服务端口发送音频帧

        :param audio_frame: 音频帧：长度1280字节，采样率16k、位长16bit、单声道，二进制数据块
        :return: None
        """
        self.ws.send(audio_frame)
        time.sleep(0.04)
        # print('Sent frame')

    def send_end_tag(self):
        """发送结束标志

        :return: None
        """
        self.ws.send(bytes(self.end_tag.encode('utf-8')))
        # print("send end tag success")

    def recv(self):
        """接受、保存、输出API返回的结果
        注意，此函数在对象构造时以附加线程的方式运行

        :return: None
        """
        try:
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    print("receive result end")
                    break
                result_dict = json.loads(result)
                self.result = result_dict
                # 解析结果
                if result_dict["action"] == "started":
                    print("handshake success, result: " + result)

                if result_dict["action"] == "result":
                    # result_1 = result_dict
                    # result_2 = json.loads(result_1["cn"])
                    # result_3 = json.loads(result_2["st"])
                    # result_4 = json.loads(result_3["rt"])
                    try:
                        # 解包API返回值
                        data_dict = json.loads(result_dict['data'])
                        output_cache = process_result_dict(data_dict, get_words=False)
                        self.outputs.append(output_cache)
                        # 控制台输出实时识别结果
                        os.system('cls')
                        # for full_sentence in self.full_sentences:
                        #     print(full_sentence, end='')
                        print(self.final_output, end='')    # 打印之前保存的结果
                        print(output_cache)     # 打印本次接收的结果
                        if data_dict["cn"]["st"]["type"] == "0":    # 判断该输出是否为最终结果
                            self.final_output += output_cache
                            self.final_words += process_result_dict(data_dict, get_words=True)
                    except:
                        print('Unwrapping result dict FAILED!')

                if result_dict["action"] == "error":
                    print("rtasr error: " + result)
                    self.ws.close()
                    return
        except websocket.WebSocketConnectionClosedException:
            print("receive result end")
            # self.recv_end_flag = True

    def close(self):
        self.ws.close()
        print("connection closed")

    # def select_full_sentence(self):
    #     while self.recv_end_flag is False or self.selected_ct < len(self.outputs) - 1:
    #         try:
    #             former_output = self.outputs[self.selected_ct]
    #             new_output = self.outputs[self.selected_ct + 1]
    #             self.selected_ct += 1
    #             if len(new_output) < 4 or \
    #                     (len(former_output) - len(new_output) > 0.4 * len(former_output) and
    #                      former_output[:4] != new_output[:4]):
    #                 self.full_sentences.append(former_output)
    #         except:
    #             pass
    #     self.full_sentences.append(self.outputs[-1])


if __name__ == '__main__':
    logging.basicConfig()

    file_path = r"./test_1.pcm"

    client = Client(app_id, api_key)
    client.send(file_path)
    client.send_end_tag()

