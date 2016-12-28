# coding: utf-8


from collections import *


class Keyword(object):
    """
    基于8-dimension情感的词
    """

    def __init__(self, word, emotion_vector):
        """
        为keyword属性赋值
        :return:
        """
        self._word = word  # 词内容
        # word_emotion_vector = [surprise, sorrow, love, joy, hate, expect, anxiety, anger]

        self._wordcount = 0
        self._wordcount += 1

        self._emotionVector = Counter()
        self._emotionVector.update({'surprise': emotion_vector['surprise']})
        self._emotionVector.update({'sorrow': emotion_vector['sorrow']})
        self._emotionVector.update({'love': emotion_vector['love']})
        self._emotionVector.update({'joy': emotion_vector['joy']})
        self._emotionVector.update({'hate': emotion_vector['hate']})
        self._emotionVector.update({'expect': emotion_vector['expect']})
        self._emotionVector.update({'anxiety': emotion_vector['anxiety']})
        self._emotionVector.update({'anger': emotion_vector['anger']})


    @property
    def word(self):
        return self._word

    @property
    def wordcount(self):
        return self._wordcount

    @property
    def emotionVector(self):
        return self._emotionVector


    def updateKeyword(self, newVector):
        """
        实现Keyword.emotionVector的更新
        :param newVector: 新的vector:Counter()
        :return:
        """
        for emotion in self._emotionVector:
            self._emotionVector[emotion] *= self._wordcount
            self._emotionVector[emotion] += newVector[emotion]

        self._wordcount += 1
        for emotion in self._emotionVector:
            self._emotionVector[emotion] /= self._wordcount
            self._emotionVector[emotion] = round(self._emotionVector[emotion], 2)

