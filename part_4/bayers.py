

def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'Love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1] #1 代表侮辱性文字 0 代表正常言论
    return postingList,classVec

def createVocabList(dataSet):
    """
    创建词汇列表
    :param dataSet:词汇
    :return: 词汇表
    """
    vocabSet = set([])  #创建一个空集
    for document in dataSet:
        vocabSet = vocabSet | set(document) #创建两个集合的并集

    return list(vocabSet)   

def setOfWords2Vec(vocabList, inputSet):
    """

    :param vocabList:词汇表
    :param inputSet:某个文档
    :return:文档向量 向量每一个元素为1或0 表示词汇表中的单词在输入文档中是否出现
    """
    returnVec = [0]*len(vocabList) #创建一个其中所含元素都为0的向量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word : %s is not in my Vocabulary!" % word)

    return returnVec
