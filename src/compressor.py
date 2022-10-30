# compressor.py
# 文本精简压缩


from numpy import *
from pyhanlp import HanLP

from rank_bm25 import BM25Okapi
from merge_repeated_words import merge


class Compressor:
    def __init__(self, text: str, words: list):
        """

        :param text: 待压缩文本
        :param words: text的分词结果
        :return: None
        """
        self.original_text = text
        self.segmented_text = words
        self.text_parse_dependence = None
        self.dependence_list = None
        self.sub_sentences_bm25_scores = []   # 查询：sub_sentences_bm25_scores[组号][index] 即为标号为 index 的子句与下一子句的相似度，末尾子句相似度记为0
        self.bm25_threshold = 3.0   # 经验数据：窗口长度为5，阈值取5.0；窗口长度为3，阈值取3.0
        self.slide_window_del_list = []
        self.dependence_del_list = []   # 根据依存句法删除的单词列表
        self.modal_verbs = ['嗯', '呃', '呢', '啊', '它这个', '他这个', '她这个', '它这种', '他这种', '她这种']
        self.text_rank_summary = None

    def slide_window_compress(self, window_length: int = 3, stride: int = 1):
        """尝试使用定长（词语个数）滑窗组成子句，然后使用BM25算法计算子句间的相似度，进而对高相似度的子句进行合并实现文本压缩。

        :param window_length: 滑窗长度（单词个数）
        :param stride: 滑动步长
        :return: None
        """
        self.bm25_threshold = float(window_length)
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
        # 取每个子句与相邻下一子句的相似度保存为对象的成员
        for group in bm25_scores:
            neighbour_scores = []
            for i in range(len(group)):
                if i + 1 < len(group):
                    neighbour_scores.append(group[i][i+1])
                else:
                    neighbour_scores.append(0.)     # 末尾子句相似度记为0
            self.sub_sentences_bm25_scores.append(neighbour_scores)

        # 计算平均BM25相似度
        # group_avg = []      # 各组的相似度均值
        # for group in self.sub_sentences_bm25_scores:
        #     group_avg.append(mean(group))
        # print(group_avg)

        # 从每组中找出并合并相似度超过某一阈值的相邻子句
        reach_threshold_flag = False
        for g in range(len(self.sub_sentences_bm25_scores)):
            if reach_threshold_flag is True:    # 完成一次片段删除后即跳出循环
                break
            for i in range(len(self.sub_sentences_bm25_scores[g])):
                # 第 g 组，第 i 个子句与相邻下一个子句相似度超过阈值
                if self.sub_sentences_bm25_scores[g][i] >= self.bm25_threshold:
                    reach_threshold_flag = True
                    # 从原始文本中删掉第 i 个子句对应的部分
                    index_to_del = stride * g + i * window_length
                    for del_cnt in range(window_length):
                        deleted_word = self.segmented_text.pop(index_to_del)
                        self.slide_window_del_list.append(deleted_word)
                        # print(deleted_word)
                    self.original_text = ''
                    for word in self.segmented_text:
                        self.original_text += word
                    # print('HERE')
                    break

        # 如果进行了片段删除，则重复递归执行该函数
        if reach_threshold_flag is True:
            # print('HERE2')
            self.sub_sentences_bm25_scores = []
            self.slide_window_compress(window_length, stride)

    def text_rank_compress(self, output_sentences: int = 3):
        """调用HanLP中的TextRank方法进行参考摘要

        :param output_sentences: 输出的句子个数
        """
        sentence_cnt = output_sentences
        while self.text_rank_summary is None and sentence_cnt > 0:
            try:
                self.text_rank_summary = HanLP.extractSummary(self.original_text, sentence_cnt)
            except:
                sentence_cnt -= 1

        if self.text_rank_summary is None:
            self.text_rank_summary = [self.original_text]

    def parse_dependence_compress(self):
        """使用HanLP.parseDependency方法对文档进行依存句法分析，然后删除特定依存类型的单词
        删除的类型：状中结构、右附加关系
        连续多个“定中关系”仅保留最后一个

        :return: None
        """
        self.text_parse_dependence = HanLP.parseDependency(self.original_text)  # HanLP依存句法分析
        dependence_list = str(self.text_parse_dependence).split('\n')
        compressed_text = ''
        for i in range(len(dependence_list)):
            cache = dependence_list[i].split()
            if len(cache) == 10:
                # 删除被归为'状中结构'和'右附加关系'的单词
                if (cache[7] == '状中结构' and (cache[3] != 'v' and cache[3] != 'c')) or cache[7] == '右附加关系':
                    self.dependence_del_list.append(cache[1])
                    dependence_list[i] = []
                # '定中关系'中词性为习语i和代词r的单词
                # elif cache[7] == '定中关系' and (cache[3] == 'i' or cache[3] == 'r'):
                #     self.dependence_del_list.append(cache[1])
                #     dependence_list[i] = []
                else:
                    dependence_list[i] = cache
                    compressed_text += cache[1]
        # 移除空元素
        for dep in dependence_list:
            if not dep:
                dependence_list.remove(dep)
        self.dependence_list = dependence_list
        self.original_text = compressed_text

    def modal_verbs_compress(self):
        """删除语气词"""
        for modal_verb in self.modal_verbs:
            self.original_text = self.original_text.replace(modal_verb, '')

    def compress(self):
        """联合调用多种方法实现文本精简压缩"""
        try:
            self.slide_window_compress(3, 1)
        except:
            pass
        try:
            self.slide_window_compress(2, 1)
        except:
            pass
        self.modal_verbs_compress()
        self.parse_dependence_compress()
        self.original_text = merge(self.original_text)
        # self.text_rank_compress(5)


if __name__ == '__main__':
    f = open('../output/speech2text/speech2text_zq.txt', encoding='utf-8')
    content = f.readlines()
    passage = ''
    words = []
    for word in content:
        passage += word[:-1]
        words.append(word[:-1])
    print(passage)
    compressor = Compressor(passage, words)
    # compressor.slide_window_compress(3, 1)
    # compressor.parse_dependence_compress()
    compressor.compress()
    print(compressor.original_text)
    print(compressor.text_rank_summary)
    # print(compressor.dependence_list)
