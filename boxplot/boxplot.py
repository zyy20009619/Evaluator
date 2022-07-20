import numpy as np


def get_percent(input):
    # 转换普通列表为数字型列表，以防出错
    input = np.array(input, dtype=np.float)
     #获取箱体图特征
    percentile = np.percentile(input, (25, 50, 75), interpolation='midpoint')
    #以下为箱线图的五个特征值
    Q1 = percentile[0] #上四分位数
    Q2 = percentile[1] #中位数
    Q3 = percentile[2] #下四分位数
    IQR = Q3 - Q1 #四分位距,即盒子的长度
    ulim = Q3 + 1.5 * IQR #上限 非异常范围内的最大值
    llim = Q1 - 1.5 * IQR #下限 非异常范围内的最小值
    # print(percentile)

    return Q1, Q2, Q3, ulim, llim