#coding=utf-8

'''
Description:
Author:
Prompt:
'''

'''
功能描述：
参数：
可参考：#https://www.cnblogs.com/fantasy01/p/4595902.html
'''
import numpy as np
from math import log
import operator
import matplotlib.pyplot as plt

#计算给定数据集的香农熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {} #定义一个字典，放label以及统计数
    for featVec in dataSet:#对数据的每一行
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0 #初始化,将当前键值加入字典
        labelCounts[currentLabel] += 1
    ShannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        ShannonEnt -= prob*log(prob, 2)
    return(ShannonEnt)

#按照给定的特征 划分数据集
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value: #将符合特征的数据抽取出来
            reducedFeatVec = featVec[:axis]#截取从0到选定的axis的各项分类信息
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)#重组一个新的dataset
    return retDataSet

#选取最好的数据集划分方式
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) -1#dataset[0] 代表索引为0的的第一行数据
    baseEntropy = calcShannonEnt(dataSet)#整个数据集的香农熵
    bestInfoGain = 0.0;#初始化
    bestFeature = -1
    for i in range(numFeatures):#循环遍历所有特征
        featList = [example[i] for example in dataSet] #先提取一行dataSet的数据，然后取该行数据的第“ i ”位元素。然后遍历每一行，最后获得一整列数据，变为一个列表list。
        uniqueVals = set(featList) #set()创建一个无序不重复元素集
        newEntropy = 0.0
        for value in uniqueVals: #计算每种划分方式的信息熵
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob*calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy#信息增益是熵的减少或者是数据无序度的减少
        if(infoGain > bestInfoGain): #计算最好的信息增益
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

#如果数据集已经处理了所有属性，但是类标签依旧不唯一，则采用多数表决的方法决定叶子节点的分类
def majorityCount(classList):
    classCount = {} #创建键值为ClassList中唯一值的数据字典，字典对象储存了classList中每个类标签出现的频率，最后利用operator操作键值排序字典
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)#key=operator.itemgetter(1) 即获取对象的第1个域的值，即统计数
    return sortedClassCount[0][0]

#利用数据集和标签列表创建树
def createTree(dataSet,  labels):
    classList = [example[-1] for example in dataSet] #取最后一列
    if classList.count(classList[0]) == len(classList): #list自带的count函数，来统计list中每个元素出现的次数，如果类别完全相同则停止继续划分
        return classList[0]
    if len(dataSet[0]) == 1: #特征属性用完了但是还没有完全分开，多数表决
        return majorityCount(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}#初始化# 注：labels列表是可变对象，在PYTHON函数中作为参数时传址引用，能够被全局修改
    # 所以这行代码导致函数外的同名变量被删除了元素，造成例句无法执行，提示'no surfacing' is not in list
    del(labels[bestFeat]) #del删除的是变量，而不是数据，当前数据集选取的最好特征存储在变量bestFeat中
    featValues = [example[bestFeat] for example in dataSet] #得到列表包含的所有属性值
    uniqueVals = set(featValues)
    for value in uniqueVals:#在每个数据集划分上递归调用函数createTree()
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat,value), subLabels)#递归调用
    return myTree

#定义文本框和箭头格式
#decisionNode = dict(boxstyle='sawtooth', fc= '0.8')#boxstyle是文本框类型 fc是边框粗细 sawtooth是锯齿形
#arrow_args = dict(arrowstyle="<-")

#绘制带箭头的注解
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt, textcoords='axes fraction',
                            va='center', ha='center', bbox=nodeType, arrowprops=arrow_args)

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

#创建绘图区，计算树形图的全局尺寸
def createPlot(inTree):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon = False, **axprops)    #no ticks
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5,1.0), '')
    plt.show()

#获取叶节点的数目
def getNumLeafs(myTree):#遍历整棵树，累计叶子节点的个数，并返回该数值，dick.keys()以列表返回一个字典所有的键
    numLeafs = 0
    firstStr = list(myTree.keys())[0]#书错 TypeError: 'dict_keys' object does not support indexing,返回的是dict_keys对象,支持iterable 但不支持indexable，我们可以将其明确的转化成list
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':#测试节点数据类型是否为字典
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

#获取树的层数
def getTreeDepth(myTree):
    depth = 0.0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > depth:
            depth = thisDepth
    return depth

#标注有向边属性
def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]#children point
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)

def plotTree(myTree, parentPt, nodeTxt):  # if the first key tells you what feat was split on

    numLeafs = getNumLeafs(myTree)  # this determines the x width of this tree
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]  # the text label for this node should be this
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':  # test to see if the nodes are dictonaires, if not they are leaf nodes
            plotTree(secondDict[key], cntrPt, str(key))  # recursion
        else:  # it's a leaf node print the leaf node
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD

if __name__=='__main__':
    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()] #inst指每一行
    print(lenses)
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
    myTree_lenses = createTree(lenses, lensesLabels)
    print(myTree_lenses)
    createPlot(myTree_lenses)
