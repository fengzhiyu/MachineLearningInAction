from math import log
import operator


def calShannonEnt(dataSet):
    """
    计算给定数据集的香农熵 公式: H = -Σ(n,i=1)p(xi)log2p(xi),其中p(xi)是选择该分类的概率
    :param dataSet: 数据集
    :return: 返回熵
    """
    numEntries = len(dataSet)#求数据长度
    labelCounts = {}#用字典来统计标签
    for featVec in dataSet:
        currentLabel = featVec[-1] #标签放在最后一个
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1

    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)

    return shannonEnt


def createDataSet():
    """
    创建数据集
    :return:数据集
    """
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']
               ]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

def spliteDataSet(dataSet, axis, value):
    """
    按给定特征划分数据集
    :param dataSet:数据集
    :param axis:需划分值在一条数据中的下标
    :param value:划分值
    :return:返回所有下标所指数据与value相同的数据集
    """
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return  retDataSet

def chooseBestFeatureToSplit(dataSet):
    """
    选择最好的数据集划分方式
    :param dataSet:数据集
    :return:返回最佳分割位置
    """
    #计算属性长度
    numFeatures = len(dataSet[0])-1
    #未划分前的熵值
    baseEntropy = calShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):
        #获取当前属性所有取值
        featList = [example[i] for example in dataSet]
        #去掉属性中重复的取值
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            #求得每种划分的信息熵
            subDataSet = spliteDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i

    return bestFeature

def majorityCnt(classList):
    """
    返回出现频率最高的分类名称
    :param classList:
    :return:
    """
    classCnt = {}
    for vote in classList:
        if vote not in classCnt.keys(): classCnt[vote] = 0
        classCnt[vote] += 1

    sortedClassCnt = sorted(classCnt.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCnt[0][0]


def creatTree(dataSet,labels):
    """
    创建树的函数代码
    :param dataSet:数据集合
    :param labels:特征值集合
    :return:一棵决策树
    """
    #获取属性取值集合
    classList = [example[-1] for example in dataSet]
    print("classList:")
    print(classList)
    print("labels:")
    print(labels)
    #当前列表中都属于同一个值，类别完全相同停止继续划分
    if classList.count(classList[0]) == len(classList):
        print("all items equals:")
        print(classList)
        return classList[0]

    if len(dataSet[0]) == 1:
        print("dataSet:")
        print(dataSet)
        print("dataSet[0]:")
        print(dataSet[0])
        return majorityCnt(classList)

    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:] #复制类标签
        myTree[bestFeatLabel][value] = creatTree(spliteDataSet(dataSet, bestFeat, value), subLabels)

    return myTree


def classify(inputTree, featLabels, testVec):
    """
    使用决策树来分类
    :param inputTree:决策树
    :param featLabels:特征表
    :param testVec:测试向量，即问题集合
    :return:返回最终的决策结果
    """
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    print("firstStr:"+firstStr)
    # print("featLabels:"+str(featLabels))
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel


def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()


def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

mydat, labels = createDataSet()
labelscopy = labels.copy()
myTree = creatTree(mydat, labels)
print(myTree)
import decision_graphic_tree
decision_graphic_tree.createPlot(myTree)
# 测试一下分类
# classlabel = classify(myTree, labelscopy,[1,0])
# print("classlabel1:"+classlabel)
# classlabel = classify(myTree, labelscopy,[1,1])
# print("classlabel2:"+classlabel)

# 选镜片分类项目
# fr = open('lenses.txt')
# lenses = [inst.strip().split('\t') for inst in fr.readlines()]
# lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
# lensesTree = creatTree(lenses, lensesLabels)
# print(lensesTree)
# import decision_graphic_tree
# decision_graphic_tree.createPlot(lensesTree)

