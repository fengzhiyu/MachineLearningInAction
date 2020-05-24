import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['simHei'] #指定默认字体 能解决中文不能正常显示的问题
#plt.rcParams['axes.unicode_minus'] = False #解决保存图像是负号‘-’显示为方块的问题

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leftNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',\
                            xytext=centerPt, textcoords='axes fraction',\
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

def createPlot(inTree):
    """
    创建树形图
    :return:
    """
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW;
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    # plotNode('决策节点', (0.5, 0.1), (0.1, 0.5), decisionNode)
    # plotNode('叶节点', (0.8, 0.1), (0.3, 0.8), leftNode)
    plt.show()


def plotMidText(cntrPt, parentPt, txtString):
    """
    在父子节点间填充信息
    :param cntrPt:
    :param parentPt:
    :param txtString:
    :return:
    """
    xMid = (parentPt[0] - cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)


def plotTree(myTree, parentPt, nodeTxt):
    """
    计算宽与高，绘制图
    :param myTree:
    :param parentPt:
    :param nodeTxt:
    :return:
    """
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff),cntrPt, leftNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD


def getNumLeafs(myTree):
    """
    获取叶节点数目
    :param myTree:
    :return:
    """
    numLeafs = 0
    # myTree.keys()不转换list将报错 -> TypeError: 'dict_keys' object does not support indexing
    firstStr = list(myTree.keys())[0]
    secondDict  = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1

    return numLeafs

def getTreeDepth(myTree):
    """
    树的层数
    :param myTree:
    :return:
    """
    maxDepth = 0
    # myTree.keys()不转换list将报错 -> TypeError: 'dict_keys' object does not support indexing
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1

        if thisDepth > maxDepth:
            maxDepth = thisDepth

    return maxDepth

def retriveTree(i):
    """
    预存树信息
    :param i:
    :return:
    """

    listOfTree = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
            {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}]
    return listOfTree[i]


