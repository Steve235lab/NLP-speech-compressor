# compressor.py
# 文本精简压缩


from numpy import *
from pyhanlp import HanLP

from rank_bm25 import BM25Okapi


class Compressor:
    def __init__(self, text: str, words: list):
        """

        :param text: 待压缩文本
        :param words: text的分词结果
        :return: None
        """
        self.original_text = text
        self.segmented_text = words
        self.text_parse_dependence = HanLP.parseDependency(self.original_text)    # HanLP依存句法分析
        dependence_list = str(self.text_parse_dependence).split('\n')
        for i in range(len(dependence_list)):
            dependence_list[i] = dependence_list[i].split()
        self.dependence_list = dependence_list
        self.sub_sentences_bm25_scores = None   # 查询：[组号][子句号1][子句号2]

    def slide_window_compress(self, window_length: int = 5, stride: int = 1):
        """尝试使用定长（词语个数）滑窗组成子句，然后使用BM25算法计算子句间的相似度，进而对高相似度的子句进行合并实现文本压缩。

        :param window_length: 滑窗长度（单词个数）
        :param stride: 滑动步长
        :return: None
        """
        # 生成子句列表
        sub_sentences = []
        for i in range(0, len(self.segmented_text)-window_length, stride):
            sub_sentence = ''
            for word in self.segmented_text[i: i+window_length]:
                sub_sentence += word
            # 以字典的形式存储子句内容与包含的单词
            cache_dict = {'sub_sentence': sub_sentence, 'words': self.segmented_text[i: i + window_length]}
            sub_sentences.append(cache_dict)

        # 对不含重叠部分的子句计算BM25相似度
        # 对子句分组，每组中子句均为不含重叠部分的子句
        grouped_sub_sentences = []
        for i in range(0, window_length // stride):
            sub_sentence_group = []
            for j in range(i, len(sub_sentences), window_length // stride):
                sub_sentence_group.append(sub_sentences[j])
            grouped_sub_sentences.append(sub_sentence_group)
        # 对每组子句之间计算BM25相似度
        bm25_scores = []  # 获取同组子句1和子句2之间的相似度：bm25_scores[组号][子句号1][子句号2]
        for group in grouped_sub_sentences:
            group_scores = []
            corpus = []
            tokenized_corpus = []
            for sub_sentence in group:
                corpus.append(sub_sentence['sub_sentence'])
                tokenized_corpus.append(sub_sentence['words'])
            bm25 = BM25Okapi(tokenized_corpus)
            for sub_sentence in group:
                group_scores.append(bm25.get_scores(sub_sentence['words']))
            bm25_scores.append(group_scores)
        self.sub_sentences_bm25_scores = bm25_scores

        # 从每组中找出相似度超过某一阈值的子句
        # 计算平均BM25相似度
        group_avg = []      # 各组的相似度均值
        for group_num in range(len(self.sub_sentences_bm25_scores)):
            avg_list = []
            for sub_sentence_num in range(len(self.sub_sentences_bm25_scores[group_num])):
                cache = self.sub_sentences_bm25_scores[group_num][sub_sentence_num]
                cache[sub_sentence_num] = 0     # 将与自己的相似度置为0，避免影响后续处理
                max_score = max(cache)      # 相似度最大值
                max_score_index = cache.argmax()    # 最相似子句标号
                print("在组", group_num, "中与子句", sub_sentence_num, "最相似的子句是：", max_score_index, "，相似度为：", max_score)
                avg_list.append(cache.mean())   # 计算均值
            group_avg.append(mean(avg_list))
        bm25_avg = mean(group_avg)  # 整体相似度均值
        print("整体BM25平均值为：", bm25_avg)
        print(grouped_sub_sentences[4][8]['sub_sentence'], grouped_sub_sentences[4][9]['sub_sentence'])


if __name__ == '__main__':
    f = open('../output/speech2text/speech2text_1665842278.txt', encoding='utf-8')
    content = f.readlines()
    passage = ''
    words = []
    for word in content:
        passage += word[:-1]
        words.append(word[:-1])
    compressor = Compressor(passage, words)
    compressor.slide_window_compress()
    # print(compressor.sub_sentences_bm25_scores)
