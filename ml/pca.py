from sklearn.decomposition import PCA
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def get_data():
    # 输入n维数据(以module级的指标先为例)
    with open(r'C:\Users\20465\Desktop\毕设相关\实验数据\度量工具结果\lanucher3\measure_result-12_notcontainIDCC.json', 'r') as f:
        json_dict = json.load(f)
    data = list()
    for module_name in json_dict:
        data.append([json_dict[module_name]['scoh'], json_dict[module_name]['scop'], json_dict[module_name]['odd'], json_dict[module_name]['idd'], json_dict[module_name]['DSM']])

    pca = PCA(n_components='mle')
    newMat = pca.fit_transform(np.array(data))
    pd.DataFrame(newMat).to_excel('output.xls')
    plt.scatter(newMat[:, 0], newMat[:, 1], marker='o')
    plt.show()


if __name__ == '__main__':
    get_data()

