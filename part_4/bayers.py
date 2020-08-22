from numpy import *


def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'Love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 代表侮辱性文字 0 代表正常言论
    return postingList, classVec

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

def trainNB0(trainMatrix, trainCategory):
    """
    朴素贝叶斯分类器训练函数
    :param trainMatrix:文档矩阵
    :param trainCategory:类别标签构成向量
    :return:
    """
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs) #负评论的概率
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    p1Vect = log(p1Num / p1Denom)
    p0Vect = log(p0Num / p0Denom)
    return p0Vect, p1Vect, pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    """
    计算概率，这里只有二分类
    :param vec2Classify:待测试词汇向量
    :param p0Vec:否定概率向量
    :param p1Vec:肯定概率向量
    :param pClass1:肯定概率值
    :return:返回一个分类结果，1或0
    """
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    """
    给定一个词汇语句，测试分类
    :return:
    """
    listOPosts, listClasses = loadDataSet() #返回已标记好的句子矩阵和对应的分类
    myVocabList = createVocabList(listOPosts)#创建一个词汇表，里面数据不重复
    trainMat = [] #列表
    for doc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, doc)) #获得语句在词汇表中出现与否的向量组成的矩阵
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses)) #计算各分类的概率，以及分类为0的概率

    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry, "  classifed as:", classifyNB(thisDoc, p0V, p1V, pAb))

    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry, " classified as:", classifyNB(thisDoc, p0V, p1V, pAb))


def bagOfWords2VecMN(vocabList, inputSet):
    """
    文档词袋模型，里面可以有重复的词
    :param vocabList:
    :param inputSet:
    :return:
    """
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec


#文件解析及完整的垃圾邮件测试函数
def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W+', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
    docList = []; classList = []; fullText = []
    for i in range(1, 26):
        wordList = textParse(open('part_4/email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('part_4/email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)

    vocabList = createVocabList(docList)
    trainingSet = list(range(50)); testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    trainMat = []; trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))
    errorCount = 0

    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1

    print('the error rate is :', float(errorCount) / len(testSet))



def calcMostFreq(vocabList, fullText):
    """
    计算出现频率
    :param vocabList:
    :param fullText:
    :return:
    """
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(), key = operator.itemgetter(1), reverse=True)
    return sortedFreq[:30]

def localWords(feed1, feed0):
    import feedparser
    docList = []; classList = []; fullText = []
    minLen = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.append(wordList)
        classList.append(0)

    createVocabList = createVocabList(docList)
    top30Words = calcMostFreq(vocabList, fullText)
    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0])

    trainningSet = range(2*minLen); testSet = []
    for i in range(20):
        randIndex = int(random.uniform(0, len(trainningSet)))
        testSet.append(trainningSet[randIndex])
        del(trainningSet[randIndex])

    trainMat = []; trainClasses = []
    for docIndex in trainningSet:
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])

    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1

    print("the error rate is:", float(errorCount) / len(testSet))
    return vocabList, p0V, p1V

def getTopWords(ny, sf):
    import operator
    vocabList, p0V, p1V = localWords(ny, sf)
    topNY = []; topSF = []
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabList[i], p0V[i]))
        if p1V[i] > -6.0 : topNY.append((vocabList[i], p1V[i]))

    sortedSF = sorted(topSF, key=lambda pair: pair[i], reverse=True)
    print("SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF")
    for item in sortedSF:
        print(item[0])

    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    print("NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY")
    for item in sortedNY:
        print(item[0])