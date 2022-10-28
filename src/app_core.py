from local_main import LocalApp


class AppCore(LocalApp):
    def get_original_text(self) -> str:
        if self.s2t is not None:
            return self.s2t.rtasr_client.final_output
        else:
            return "等待语音输入..."

    def get_compressed_text(self) -> str:
        if self.compressor is not None:
            return self.compressor.original_text
        else:
            return "等待精简摘要完成..."


APP_CORE = AppCore()
