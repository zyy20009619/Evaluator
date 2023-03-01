import os

from util.csv_operator import read_csv_folder
from util.metrics import *
import pandas as pd


def detect_change(det, output):
    class_aosp_res, class_not_aosp_res, method_aosp_res, method_not_aosp_res, ownership_res = read_csv_folder(det,
                                                                                                              'measure_result_class_aosp.csv',
                                                                                                              'measure_result_class_not_aosp.csv',
                                                                                                              'measure_result_method_aosp.csv',
                                                                                                              'measure_result_method_not_aosp.csv',
                                                                                                              'final_ownership.csv')
    # if not (class_aosp_res or class_not_aosp_res or method_aosp_res or method_not_aosp_res or ownership_res):
    #     return False
    # 1.过滤伴生实体中的侵入式实体
    intrusive_res = ownership_res.loc[ownership_res['isIntrusive'] == 1]
    intrusive_class_res = intrusive_res.loc[intrusive_res['category'] == 'Class']['qualifiedName']
    intrusive_method_res = intrusive_res.loc[intrusive_res['category'] == 'Method']['qualifiedName']
    intrusive_class_not_aosp_res = class_not_aosp_res.loc[class_not_aosp_res['class_name'].isin(intrusive_class_res)]
    intrusive_method_not_aosp_res = method_not_aosp_res.loc[
        method_not_aosp_res['method_name'].isin(intrusive_method_res)]
    # 2.对比伴生修改后的原生质量
    CLASS_METRICS.append('class_name')
    METHOD_METRICS.append('method_name')
    merge_intrusive_class_not_aosp_res = pd.merge(class_aosp_res[CLASS_METRICS],
                                                  intrusive_class_not_aosp_res[CLASS_METRICS],
                                                  how='inner', left_on=['class_name'],
                                                  right_on=['class_name'], suffixes=['1', ''])
    merge_class_name = merge_intrusive_class_not_aosp_res['class_name']
    diff_intrusive_class_not_aosp_res = merge_intrusive_class_not_aosp_res.drop(['class_name'], axis=1).diff(periods=42,
                                                                                                             axis=1).iloc[
                                        :, 42:]
    diff_intrusive_class_not_aosp_res.insert(0, 'class_name', merge_class_name)
    diff_intrusive_class_not_aosp_res.to_csv(os.path.join(output, "diff_intrusive_class_not_aosp_res.csv"), index=False,
                                             sep=',')
    merge_intrusive_method_not_aosp_res = pd.merge(method_aosp_res[METHOD_METRICS],
                                                   intrusive_method_not_aosp_res[METHOD_METRICS], how='inner',
                                                   left_on=['method_name'],
                                                   right_on=['method_name'], suffixes=['1', ''])
    merge_method_name = merge_intrusive_method_not_aosp_res['method_name']
    diff_intrusive_method_not_aosp_res = merge_intrusive_method_not_aosp_res.drop(['method_name'], axis=1).diff(
        periods=13,
        axis=1).iloc[:, 13:]
    diff_intrusive_method_not_aosp_res.insert(0, 'method_name', merge_method_name)
    diff_intrusive_method_not_aosp_res.to_csv(os.path.join(output, "diff_intrusive_method_not_aosp_res.csv"),
                                              index=False,
                                              sep=',')
    return True
