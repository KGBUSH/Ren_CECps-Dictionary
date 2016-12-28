# coding: utf-8


import os
from os.path import join



class AdjustCoding(object):
    """
    调整编码
    """

    @staticmethod
    def adjust_coding(folder):
        """
        判断.xml文件的编码，调整
        :param folder: .xml所在的目标文件夹
        :return:
        """

        for root, dirs, files in os.walk(folder):
            for OneFileName in files:
                if OneFileName.find('.xml') == -1:
                    continue
                OneFullFileName = join(root, OneFileName)
                print OneFullFileName

                fr = open(OneFullFileName, 'r')
                content = fr.read()
                fr.close()

                if content.find('GB2312') == -1:
                    continue
                else:
                    # 改编码，以及第一行的encoding属性
                    content = content.decode('GB2312', 'ignore').encode('UTF-8')
                    content = content.replace('GB2312', 'UTF-8')
                    fw = open(OneFullFileName, 'w')
                    fw.write(content)
                    fw.close()





if __name__ == '__main__':
    folder = 'C:\\Users\\KGBUS\\PycharmProjects\\RenCEC-Dictionary\\data\\CEC_emotionCoprus'
    AdjustCoding.adjust_coding(folder=folder)