# merge_repeated_words.py
# 合并文本中连续重复的词


# from word_segment import WordSegment


# def merge(sentence: str) -> str:
#     """合并文本中连续重复的词
#
#     """
#     ws = WordSegment(sentence)
#     ws.fully_segment()
#     merged_sentence = ''
#     index = 0
#     while index < len(ws.words) - 1:
#         if ws.words[index] != ws.words[index+1]:
#             merged_sentence += ws.words[index]
#         index += 1
#
#     return merged_sentence

def merge(sentence, max_ngram_length=4):
    """基于ngram合并文本中连续重复的词

    方法来源：https://zhuanlan.zhihu.com/p/99781056
    """
    final_merge_sent = sentence
    max_ngram_length = min(max_ngram_length, len(sentence))
    for i in range(max_ngram_length, 0, -1):
        start = 0
        end = len(final_merge_sent) - i + 1
        ngrams = []
        while start < end:
            ngrams.append(final_merge_sent[start: start + i])
            start += 1
        result = []
        for cur_word in ngrams:
            result.append(cur_word)
            if len(result) > i:
                pre_word = result[len(result) - i - 1]
                if pre_word == cur_word:
                    for k in range(i):
                        result.pop()

        cur_merge_sent = ""
        for word in result:
            if not cur_merge_sent:
                cur_merge_sent += word
            else:
                cur_merge_sent += word[-1]
        final_merge_sent = cur_merge_sent

    return final_merge_sent


if __name__ == '__main__':
    text = '你是一个一个一个'
    print(merge(text))
