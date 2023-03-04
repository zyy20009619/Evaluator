import os

from util.csv_operator import read_csv_folder
from util.metrics import *
import pandas as pd
from util.json_operator import read_file
from util.path_operator import create_file_path


def detect_change(path1, path2, output):
    base_out = create_file_path(os.path.join(output, 'analyseResult'), '')
    # 读取原生数据和伴生数据
    class_aosp_res, class_not_aosp_res, method_aosp_res, method_not_aosp_res = read_csv_folder(os.path.join(path1, 'measure_result_class.csv'),
                                                                                                              os.path.join(path2, 'measure_result_class.csv'),
                                                                                                              os.path.join(path1, 'measure_result_method.csv'),
                                                                                                              os.path.join(path2, 'measure_result_method.csv'))
    # 读取耦合切面数据
    facade_data = read_file(os.path.join(path2, 'facade.json'))
    # 从耦合切面数据中抽取伴生项目中所有类/方法实体的实体归属方
    ownership_res = list()
    for facade in facade_data['res']:
        for item in facade_data['res'][facade]:
            if item['src']['category'] == 'Class' or item['src']['category'] == 'Method':
                ownership_res.append([item['src']['qualifiedName'], item['src']['category'], item['src']['ownership']])
            if item['dest']['category'] == 'Class' or item['dest']['category'] == 'Method':
                ownership_res.append([item['dest']['qualifiedName'], item['dest']['category'], item['dest']['ownership']])
    # 对关注类实体进行质量扫描
    entity_pd = pd.DataFrame(ownership_res, columns=['qualifiedName', 'category', 'ownership'])
    entity_pd.drop_duplicates(subset=['qualifiedName'], keep='first', inplace=True)
    entity_pd.to_csv(os.path.join(base_out, "ownership_data.csv"), index=False, sep=',')
    CLASS_METRICS.append('class_name')

    intrusive_class = entity_pd[(entity_pd['category'] == 'Class') & (entity_pd['ownership'] == 'intrusive native')]['qualifiedName']
    intrusive_class_measure = class_not_aosp_res.loc[class_not_aosp_res['class_name'].isin(intrusive_class)]
    merge_intrusive_class = pd.merge(class_aosp_res[CLASS_METRICS], intrusive_class_measure[CLASS_METRICS],
                                                  how='inner', left_on=['class_name'],
                                                  right_on=['class_name'], suffixes=['1', ''])
    merge_class_name = merge_intrusive_class['class_name']
    diff_intrusive_class = merge_intrusive_class.drop(['class_name'], axis=1).diff(periods=42, axis=1).iloc[:, 42:]
    diff_intrusive_class.insert(0, 'class_name', merge_class_name)
    diff_intrusive_class.sort_values(by="CBC", inplace=True, ascending=False)
    diff_intrusive_class.to_csv(os.path.join(base_out, "diff_intrusive_class.csv"), index=False, sep=',')
    diff_intrusive_class_
    

    actively_class = entity_pd[(entity_pd['category'] == 'Class') & (entity_pd['ownership'] == 'actively native')]['qualifiedName']
    actively_class_measure = class_not_aosp_res.loc[class_not_aosp_res['class_name'].isin(actively_class)]
    merge_actively_class = pd.merge(class_aosp_res[CLASS_METRICS], actively_class_measure[CLASS_METRICS],
                                     how='inner', left_on=['class_name'],
                                     right_on=['class_name'], suffixes=['1', ''])
    merge_class_name = merge_actively_class['class_name']
    diff_actively_class = merge_actively_class.drop(['class_name'], axis=1).diff(periods=42, axis=1).iloc[:, 42:]
    diff_actively_class.insert(0, 'class_name', merge_class_name)
    diff_actively_class.sort_values(by="CBC", inplace=True, ascending=False)
    diff_actively_class.to_csv(os.path.join(base_out, "diff_actively_class.csv"), index=False, sep=',')
    # 对产生腐化的类实体进行定位（根据腐化严重程度进行输出）

    # intrusive_method = entity_pd[(entity_pd['category'] == 'Method') & (entity_pd['ownership'] == 'intrusive native')][
    #     'qualifiedName']
    # actively_method = entity_pd[(entity_pd['category'] == 'Method') & (entity_pd['ownership'] == 'actively native')][
    #     'qualifiedName']
    # intrusive_method_measure = method_not_aosp_res.loc[method_not_aosp_res['method_name'].isin(intrusive_method)]
    # actively_method_measure = method_not_aosp_res.loc[method_not_aosp_res['method_name'].isin(actively_method)]
    # METHOD_METRICS.append('method_name')
    # # 对关注方法实体进行质量扫描
    # merge_intrusive_method = pd.merge(method_aosp_res[METHOD_METRICS], intrusive_method_measure[METHOD_METRICS],
    #                                  how='inner', left_on=['method_name'],
    #                                  right_on=['method_name'], suffixes=['1', ''])
    # merge_method_name = merge_intrusive_method['method_name']
    # diff_intrusive_method = merge_intrusive_method.drop(['method_name'], axis=1).diff(periods=42, axis=1).iloc[:, 42:]
    # diff_intrusive_method.insert(0, 'method_name', merge_method_name)
    # diff_intrusive_method.to_csv(os.path.join(base_out, "diff_intrusive_method.csv"), index=False, sep=',')
    #
    # merge_actively_method = pd.merge(method_aosp_res[METHOD_METRICS], actively_method_measure[METHOD_METRICS],
    #                                 how='inner', left_on=['method_name'],
    #                                 right_on=['method_name'], suffixes=['1', ''])
    # merge_method_name = merge_actively_method['method_name']
    # diff_actively_method = merge_actively_class.drop(['method_name'], axis=1).diff(periods=42, axis=1).iloc[:, 42:]
    # diff_actively_method.insert(0, 'method_name', merge_method_name)
    # diff_actively_method.to_csv(os.path.join(base_out, "diff_actively_method.csv"), index=False, sep=',')

    return True


