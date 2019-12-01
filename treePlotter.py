#coding=utf-8

'''
Description:
Author:
Prompt:
'''

'''
功能描述：绘制树节点
参数：
'''

#使用文本绘制树节点
import matplotlib.pyplot as plt
#定义文本框和箭头格式
decisionNode = dict(boxstyle='sawtooth', fc= '0.8')#boxstyle是文本框类型 fc是边框粗细 sawtooth是锯齿形
leafNode = dict(boxstyle='round4', fc= '0.8')
arrow_args = dict(arrowstyle="<-")

#plotNode函数执行了实际的绘图功能
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    '''
    这个是用来以注释形式绘制节点和箭头线，可以不用细看
    这个函数原型是class matplotlib.axes.Axes()的成员函数annotate()
    该函数的作用是为绘制的图上指定的数据点xy添加一个注释nodeTxt,注释的位置由xytext指定
    其中，xycoords来指定点xy坐标的类型，textcoords指定xytext的类型，xycoords和textcoords的取值如下：
    ‘figure points’：此时坐标表示坐标原点在图的左下角的数据点
    ‘figure pixels’：此时坐标表示坐标原点在图的左下角的像素点
    ‘figure fraction’：此时取值是小数，范围是([0, 1], [0, 1]) ，在图的最左下角时xy是(0,0), 最右上角是(1, 1) ，其他位置按相对图的宽高的比例取小数值
    ‘axes points’：此时坐标表示坐标原点在图中坐标的左下角的数据点
    ‘axes pixels’：此时坐标表示坐标原点在图中坐标的左下角的像素点
    ‘axes fraction’：类似‘figure fraction’，只不过相对图的位置改成是相对坐标轴的位置
    ‘data’：此时使用被注释的对象所采用的坐标系（这是默认设置），被注释的对象就是调用annotate这个函数
     那个实例，这里是ax1，是Axes类，采用ax1所采用的坐标系
    ‘offset points’：此时坐标表示相对xy的偏移（以点的个数计），不过一般这个是用在textcoords
    ‘polar’：极坐标类型，在直角坐标系下面也可以用，此时坐标含义为(theta, r)
     参数arrowprops含义为连接数据点和注释的箭头的类型，该参数是dictionary类型，该参数含有一个
     名为arrowstyle的键，一旦指定该键就会创建一个class matplotlib.patches.FancyArrowPatch类的实例
     该键取值可以是一个可用的arrowstyle名字的字符串，也可以是可用的class matplotlib.patches.ArrowStyle类的实例
     具体arrowstyle名字的字符串可以参考
     http://matplotlib.org/api/patches_api.html#matplotlib.patches.FancyArrowPatch
    里面的class matplotlib.patches.FancyArrowPatch类的arrowstyle参数设置
    函数返回一个类class matplotlib.text.Annotation()的实例
    '''
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt, textcoords='axes fraction',va='center', ha='center', bbox=nodeType, arrowprops=arrow_args)

def createPlot():#绘制，首先创建新图形并且清空绘画区，然后在绘画区绘制两个代表不同类型的树节点
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
    fig = plt.figure(1, facecolor='white')  # 创建新的figure 1, 背景颜色为白色
    fig.clf()  # 清空figure 1的内容
    createPlot.ax1 = plt.subplot(111, frameon=False)
    plotNode('决策节点', (0.5, 0.1), (0.1, 0.5),  decisionNode)
    plotNode('叶节点', (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()

if __name__=='__main__':
    print(createPlot())