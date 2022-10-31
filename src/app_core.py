from local_main import LocalApp


class AppCore(LocalApp):
    def get_original_text(self) -> str:
        if self.s2t is not None:
            return self.s2t.rtasr_client.final_output
        else:
            return "等待语音输入..."

    def get_compressed_text(self) -> str:
        if len(self.compressor.original_text) > 0:
            return self.compressor.original_text
        else:
            return "未检测到已录入文本，请先录入文本！"

    def get_text_rank_output(self) -> str:
        if self.compressor.text_rank_summary is None:
            return "未检测到已录入文本，请先录入文本！"
        else:
            summary_str = ''
            cache = self.compressor.text_rank_summary
            for summary in cache:
                summary_str += '* ' + summary + '\n'
            return summary_str


APP_CORE = AppCore()
