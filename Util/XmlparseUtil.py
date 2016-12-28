# coding: utf-8

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from Entity.Keyword import *
import os
from os.path import join
from collections import *



def CountFolder_Files(destfolder):
    """
    计算目标文件夹下面的文件总数
    :param destfolder: 目录
    :return:
    """
    count = 0  # 计数
    for root, dirs, files in os.walk(destfolder):
        filenum = len(files)
        if filenum != 0:
            count += filenum

    return count





class XmlparseUtil(object):
    """
    分析xml构建 情感词典
    """
    def __init__(self, xmlfolder):
        """
        初始化一些参数
        :param xmlfolder: .xml所在的目标文件夹
        :return:
        """
        self.keywordsList = []
        self.wordsList = []
        self.xmlFolder = xmlfolder
        self.countXml = CountFolder_Files(destfolder=xmlfolder)  # 总共的xml文件数量



    def Extract_Keywords(self):
        """
        读取folder中的所有.xml，提取keyword
        :return:
        """
        print 'Now doing Extract_Keywords.'
        count = 0
        for root, dirs, files in os.walk(self.xmlFolder):
            for OneFileName in files:
                if OneFileName.find('.xml') == -1:
                    continue
                OneFullFileName = join(root, OneFileName)
                tree = ET.ElementTree(file=OneFullFileName)

                for element in tree.iterfind('.//Keywords'):
                    now_word = element.text
                    if len(now_word) <= 1:
                        continue
                    newVector = Counter()
                    newVector.update({'surprise': float(element.get('Surprise'))})
                    newVector.update({'sorrow': float(element.get('Sorrow'))})
                    newVector.update({'love': float(element.get('Love'))})
                    newVector.update({'joy': float(element.get('Joy'))})
                    newVector.update({'hate': float(element.get('Hate'))})
                    newVector.update({'expect': float(element.get('Expect'))})
                    newVector.update({'anxiety': float(element.get('Anxiety'))})
                    newVector.update({'anger': float(element.get('Anger'))})

                    if now_word in self.wordsList:  # 如果已经记录过这个词
                        for keyword in self.keywordsList:
                            if keyword.word == now_word:
                                keyword.updateKeyword(newVector)
                                break
                    else:
                        self.wordsList.append(now_word)
                        new_keyword = Keyword(word=now_word, emotion_vector=newVector)
                        self.keywordsList.append(new_keyword)

                if count % 50 == 0:
                    print str(count), '/', str(self.countXml)
                count += 1


    def ShowKeywords(self):
        """
        打印结果
        :return:
        """
        for keyword in self.keywordsList:
            print keyword.word, '  ',
            print str(keyword.wordcount), '  '
            print keyword.emotionVector


    def Output(self, dest):
        """
        输出结果到文件中
        :param dest: 生成文件的位置
        :return:
        """
        print '\n\n', 'Now writing to file.'
        total_keywords = len(self.wordsList)
        num = 0
        try:
            fw = open(dest, 'w')
            for keyword in self.keywordsList:
                str_keyword = keyword.word + '  ,  ' + str(keyword.wordcount) \
                              + '  ,  ' + str(keyword.emotionVector)[8:-1]
                fw.write(str_keyword.encode('utf-8') + '\n')
                num += 1
                if num % 100 == 0:
                    print str(num), '/', str(total_keywords)
            fw.close()
        except Exception, e:
            print 'Output: Exception', e


    def special_Output(self, dest):
        """
        打印出各因子下的前100名的词
        :param dest: 输出文件的位置
        :return:
        """
        print '\n', 'Now doing Special Output.'
        try:
            # fw = open(dest, 'w')
            eightEmotions = ['surprise', 'sorrow', 'love', 'joy', 'hate', 'expect', 'anxiety', 'anger']  # 八种情绪
            for emotion in eightEmotions:
                print 'Here is ', emotion
                # fw.write('Here is ' + emotion + '\n')
                now_emotion_keywordsList = sorted(self.keywordsList, key=lambda Keyword:Keyword.emotionVector[emotion], reverse=True)
                emoCounter = Counter()
                for i in xrange(500):
                    keyword = now_emotion_keywordsList[i]
                    emoCounter += keyword.emotionVector
                    str_keyword = keyword.word + '  ,  ' + str(keyword.wordcount)\
                                  + '  ,  ' + str(keyword.emotionVector)[8:-1]
                    # fw.write(str_keyword.encode('utf-8') + '\n')
                print emoCounter
                # fw.write('\n')
            # fw.close()
        except Exception, e:
            print 'special_Output: Exception', e






if __name__ == '__main__':
    xmlfolder = 'C:\\Users\\KGBUS\\PycharmProjects\\RenCEC-Dictionary\\data\\CEC_emotionCoprus'
    testxmlfolder = 'C:\\Users\\KGBUS\\PycharmProjects\\RenCEC-Dictionary\\data\\test'
    x = XmlparseUtil(xmlfolder=xmlfolder)
    x.Extract_Keywords()
    # x.ShowKeywords()
    # x.Output('C:\\Users\\KGBUS\\PycharmProjects\\RenCEC-Dictionary\\data\\generatedFile\\dictCEC.txt')
    x.special_Output('C:\\Users\\KGBUS\\PycharmProjects\\RenCEC-Dictionary\\data\\generatedFile\\sorted_dictCEC.txt')
