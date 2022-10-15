# word_segment.py
# 文本分词功能模块


from load_dictionary import load_dictionary


class WordSegment:
    def __init__(self, text):
        self.original_text = text
        self.words = []
        self.mini_dic = load_dictionary()

    def fully_segment(self):
        """完全切分

        """
        word_list = []
        for i in range(len(self.original_text)):  # i 从 0 到text的最后一个字的下标遍历
            for j in range(i + 1, len(self.original_text) + 1):  # j 遍历[i + 1, len(text)]区间
                word = self.original_text[i:j]  # 取出连续区间[i, j]对应的字符串
                if word in self.mini_dic:  # 如果在词典中，则认为是一个词
                    word_list.append(word)
        self.words = word_list
