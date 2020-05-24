from numpy import *
import operator

import matplotlib
import matplotlib.pyplot as plt

from os import listdir

def createDataSet():
    """
    创建数据及其标签
    :return:
    """
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B',  'B']
    return group, labels


def classify0(inX, dataSet, labels, k):
    """
    k-近邻算法实现
    :param inX:特征值
    :param dataSet:数据集
    :param labels:标注的分类结果
    :param k:求前k个
    :return:前k个距离最近的选项中,返回出现频率最大的项
    """
    # 返回数据集中行的大小
    dataSetSize = dataSet.shape[0]
    #将输入参数inX扩展到与数据集行的大小一致的矩阵，然后每项做差
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    #求差值后的矩阵每项乘方
    sqDiffMat = diffMat**2
    #以行为单位，求和
    sqDistances = sqDiffMat.sum(axis=1)
    #开方，计算距离
    distances = sqDistances**0.5
    #按从小到大次序排序，保存对应的下标值
    sortedDistances = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistances[i]] #取得在前k个距离下的对应取值
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1 #计算当前取值voteIlabel的个数,get()如果获取不到，默认为0

    # 在python2.x版本中使用iteritems,operator.itemgetter(1)是以第二个项进行排序,这里是逆序
    sortedClassCount = sorted(classCount.items(),
                              key = operator.itemgetter(1),reverse = True)
    #最后返回第一项的第一个属性值 sortedClassCount {'A':3,'B':1}
    return sortedClassCount[0][0]


def file2matrix(filename, size = 3):
    """
    读取文件中的数据到矩阵和列表中
    :param filename:
    :return:
    """
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines,size))
    classLabelVector = []
    index = 0

    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:size]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector


def autoNorm(dataSet):
    """
    归一化
    :param dataSet:
    :return:
    """
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet, ranges, minVals

def datingClassTest():
    """
    求准确率
    :return:
    """
    hoRatio = 0.05
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normData, ranges, minVals = autoNorm(datingDataMat)
    m = normData.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normData[i,:],normData[numTestVecs:m,:], datingLabels[numTestVecs:m],3)
        print("the calssifier came back with:%d,the real answer is %d"%(classifierResult,datingLabels[i]))
        if (classifierResult != datingLabels[i]): errorCount += 1.0

    print("the total error rate is: %f " % (errorCount/float(numTestVecs)))

def classifyPerson():
    """
    输入某人的数据进行测试是否有机会约会，K-近邻算法
    :return:
    """
    resultList = ['not at all','in small doses','in large doses']
    percentTats = float(input("percentage of time spent playing viedo games?"))
    ffMiles = float(input("frequent filer miles earned per years?"))
    iceCream = float(input("liters of ice cream consumed per years?"))
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)

    intArr = array([ffMiles,percentTats,iceCream])
    classRes = classify0((intArr-minVals)/ranges,normMat,datingLabels,3)
    print("you will probably like this person:",resultList[classRes-1])

def img2Vector(filename):
    """
    将图像转换成向量，32*32 -> 1*1024
    :param filename:
    :return:
    """
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect


def handWritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2Vector('trainingDigits/%s' % fileNameStr)

    testFileList = listdir('testDigits')
    errorCount = 0.0

    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2Vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest,trainingMat,hwLabels,3)

        print("the classifier came back with %d,the real answer is:%d "%(classifierResult,classNumStr))
        if classNumStr!=classifierResult: errorCount += 1.0

    print("\n error count:%f" % errorCount)
    print("\n error rate:%f" % (errorCount/float(mTest)))


if __name__ == '__main__':
    # group,labels = createDataSet()
    # print(classify0([0,0],group,labels,3))
    #
    # datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.scatter(datingDataMat[:, 0],datingDataMat[:, 1],
    #            15.0*array(datingLabels), 15.0*array(datingLabels))
    # plt.show()
    #
    # normData, range, minVals = autoNorm(datingDataMat)
    # print(normData)
    # print(range)
    # print(minVals)
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.scatter(normData[:, 0], normData[:, 1],
    #            15.0 * array(datingLabels), 15.0 * array(datingLabels))
    # plt.show()

    #datingClassTest()
    #classifyPerson()

    handWritingClassTest()#手写字符识别准确率