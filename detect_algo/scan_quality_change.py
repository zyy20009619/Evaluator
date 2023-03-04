import os
from util.csv_operator import read_csv_folder
from util.metrics import *
import pandas as pd
from util.json_operator import read_file
from util.path_operator import create_file_path

MODULE_METRICS.append('module_name')
CLASS_METRICS.append('class_name')
METHOD_METRICS = ['class_name', 'method_name', 'CBM', 'm_FAN_IN', 'm_FAN_OUT', 'IDMC', 'EDMC']


# 检测安卓扩展场景和一般场景腐化问题及根因
def detect_change(path1, path2, output, opt):
    base_out = create_file_path(os.path.join(output, 'analyseResult'), '')
    # 读取path1和path2数据
    class1_res, class2_res, method1_res, method2_res = read_csv_folder(
        os.path.join(path1, 'measure_result_class.csv'),
        os.path.join(path2, 'measure_result_class.csv'),
        os.path.join(path1, 'measure_result_method.csv'),
        os.path.join(path2, 'measure_result_method.csv'))
    # 获取到所有粒度实体的质量diff，类和方法粒度的diff包含三种状态：add/modify/delete
    merge_class_left = pd.merge(class2_res, class1_res,
                                 how='left', left_on=['class_name'],
                                 right_on=['class_name'], suffixes=['1', ''])
    merge_name_left = merge_class_left[['module_name', 'class_name']]
    diff_class_left = merge_class_left.drop(['module_name', 'module_name1', 'class_name'], axis=1).diff(periods=65,
                                                                                                          axis=1).iloc[:, 65:]
    diff_class = pd.concat([merge_name_left, diff_class_left], axis=1)
    # 只包含修改类的数据(应该包含所有类：被修改/被增加/被删除)
    diff_class = diff_class.dropna(axis=0, how='any')
    # diff_class['status'] = 'modify'
    # add_class =
    # delete_class =

    merge_method = pd.merge(method2_res[METHOD_METRICS], method1_res[METHOD_METRICS],
                            how='left', left_on=['method_name'],
                            right_on=['method_name'], suffixes=['1', ''])
    merge_name = merge_method[['class_name', 'method_name']]
    diff_method = merge_method.drop(['class_name1', 'class_name', 'method_name'], axis=1).diff(periods=5, axis=1).iloc[
                  :, 5:]
    method_name_and_startLine = method2_res[['method_name', 'startLine']]
    diff_method = pd.concat([merge_name, diff_method], axis=1)
    diff_method = pd.merge(method_name_and_startLine, diff_method, on='method_name')
    # 只包含修改方法的数据(应该包含所有方法：被修改/被增加/被删除)
    diff_method = diff_method.dropna(axis=0, how='any')
    # 分别对扩展场景和一般场景进行不同逻辑处理
    if opt == 'extension':
        # 读取耦合切面数据
        facade_data = read_file(os.path.join(path2, 'facade.json'))
        res = detect_android_project(base_out, facade_data, diff_class, diff_method, opt)
    else:
        res = detect_common_project(base_out, diff_class, diff_method, opt)
    res.to_csv(os.path.join(base_out, "detection result.csv"), index=False, sep=',')
    # # 统计检测结果数据
    # count_pd = pd.DataFrame()
    #
    # count_pd.to_csv(os.path.join(base_out, "detection count.csv"), index=False, sep=',')


def detect_android_project(base_out, facade_data, diff_class, diff_method, opt):
    # 从耦合切面数据中抽取伴生项目中所有类/方法实体的实体归属方
    ownership_res = list()
    for facade in facade_data['res']:
        for item in facade_data['res'][facade]:
            if item['src']['category'] == 'Class' or item['src']['category'] == 'Method':
                ownership_res.append([item['src']['qualifiedName'], item['src']['category'], item['src']['ownership']])
            if item['dest']['category'] == 'Class' or item['dest']['category'] == 'Method':
                ownership_res.append(
                    [item['dest']['qualifiedName'], item['dest']['category'], item['dest']['ownership']])
    # 构造所有类和方法实体的归属方dataframe
    entity_pd = pd.DataFrame(ownership_res, columns=['qualifiedName', 'category', 'ownership'])
    entity_pd.drop_duplicates(subset=['qualifiedName'], keep='first', inplace=True)
    entity_pd.to_csv(os.path.join(base_out, "ownership data.csv"), index=False, sep=',')

    # 为所有方法实体的质量diff赋予归属方信息并输出
    method_ownership = entity_pd[entity_pd['category'] == 'Method'][['qualifiedName', 'ownership']].rename(
        columns={'qualifiedName': 'method_name'})
    diff_method = pd.merge(method_ownership, diff_method, on='method_name')
    diff_method.to_csv(os.path.join(base_out, "diff ownership method.csv"), index=False, sep=',')

    # 获取到intrusive native和actively native类实体的质量diff并对腐化实体进行根因定位
    intrusive_res_pd = get_android_decay_root_cause(entity_pd, 'intrusive native', diff_class, base_out,
                                            diff_method, opt)
    actively_res_pd = get_android_decay_root_cause(entity_pd, 'actively native', diff_class, base_out, diff_method, opt)
    res_pd = pd.concat([intrusive_res_pd, actively_res_pd], axis=0)
    res_pd = res_pd.rename(
        columns={'CBC': 'class decay degree', 'CBM': 'method decay degree', 'ownership': 'method_ownership',
                 'class_name': 'problem class', 'method_name': 'problem method'})
    return res_pd


def detect_common_project(base_out, diff_class, diff_method, opt):
    # 输出所有class diff信息
    diff_class.to_csv(os.path.join(base_out, "diff class.csv"), index=False, sep=',')
    # 输出所有method diff信息
    diff_method.to_csv(os.path.join(base_out, "diff method.csv"), index=False, sep=',')
    return get_common_decay_root_cause(diff_class, diff_method, opt)


def get_android_decay_root_cause(ownership_pd, ownership, diff_class, base_out, diff_method, opt):
    ownership_class = ownership_pd[(ownership_pd['category'] == 'Class') & (ownership_pd['ownership'] == ownership)][
        'qualifiedName']
    ownership_diff_class_measure = diff_class.loc[diff_class['class_name'].isin(ownership_class)]
    ownership_diff_class_measure.sort_values(by="CBC", inplace=True, ascending=False)
    ownership_diff_class_measure.to_csv(os.path.join(base_out, 'diff ' + ownership + '.csv'), index=False, sep=',')
    # 对产生腐化的类实体进行定位（根据腐化严重程度进行输出）
    coupling_df = detect_coupling_problem(diff_class, diff_method, opt)
    del coupling_df['scop']
    cohesion_df = detect_cohesion_problem(diff_class, diff_method, opt)
    del coupling_df['scoh']
    res_pd = pd.concat([coupling_df, cohesion_df], axis=0)
    res_pd.insert(0, 'class_ownership', ownership)
    return res_pd


def get_common_decay_root_cause(diff_class, diff_method, opt):
    # 对产生腐化的模块实体进行定位（根据腐化严重程度进行输出）
    diff_class.sort_values(by="scop", inplace=True, ascending=False)
    coupling_df = detect_coupling_problem(diff_class[diff_class['scop'] > 0], diff_method, opt)
    coupling_df = coupling_df.rename(
        columns={'scop': 'module decay degree'})
    diff_class.sort_values(by="scoh", inplace=True, ascending=True)
    cohesion_df = detect_cohesion_problem(diff_class[diff_class['scoh'] < 0], diff_method, opt)
    cohesion_df = cohesion_df.rename(
        columns={'scoh': 'module decay degree'})
    res_pd = pd.concat([coupling_df, cohesion_df], axis=0)
    res_pd = res_pd.rename(
        columns={'CBC': 'class decay degree', 'CBM': 'method decay degree',
                 'class_name': 'problem class', 'method_name': 'problem method'})
    return res_pd


def detect_coupling_problem(diff_class_measure, diff_method_measure, opt):
    # 规则集1：检测与外部的耦合情况
    diff_coupling_decay_class = diff_class_measure[
        (diff_class_measure['CBC'] > 0) & (diff_class_measure['EDCC'] > 0.4 * diff_class_measure['CBC'])]
    diff_coupling_inherit_decay_class = diff_coupling_decay_class[
        (diff_coupling_decay_class['c_FAN_OUT'] > 0) & (diff_coupling_decay_class['NAC'] > 0) |
        (diff_coupling_decay_class['c_FAN_IN'] > 0) & (diff_coupling_decay_class['NDC'] > 0)]

    diff_coupling_import_decay_class = diff_coupling_decay_class[
        (diff_coupling_decay_class['c_FAN_OUT'] > 0) & (diff_coupling_decay_class['NOI'] > 0) |
        (diff_coupling_decay_class['c_FAN_IN'] > 0) & (diff_coupling_decay_class['NOID'] > 0)]

    diff_merge_class_and_method = pd.merge(diff_method_measure, diff_coupling_decay_class, on='class_name')
    diff_coupling_call_decay_class = diff_merge_class_and_method[
        (diff_merge_class_and_method['c_FAN_OUT'] > 0) & (diff_merge_class_and_method['CBM'] > 0) & (
                diff_merge_class_and_method['EDMC'] > 0) & (diff_merge_class_and_method['m_FAN_OUT'] > 0) |
        (diff_merge_class_and_method['c_FAN_IN'] > 0) & (diff_merge_class_and_method['CBM'] > 0) & (
                diff_merge_class_and_method['EDMC'] > 0) & (diff_merge_class_and_method['m_FAN_IN'] > 0)]

    return set_root_cause(diff_coupling_import_decay_class, diff_coupling_inherit_decay_class, diff_coupling_call_decay_class, opt, 'coupling')


def detect_cohesion_problem(diff_class_measure, diff_method_measure, opt):
    # 规则集2：检测内聚情况
    diff_cohesion_decay_class = diff_class_measure[diff_class_measure['IDCC'] < 0]
    diff_cohesion_inherit_decay_class = diff_cohesion_decay_class[
        (diff_cohesion_decay_class['IODD'] < 0) & (diff_cohesion_decay_class['NAC'] < 0) |
        (diff_cohesion_decay_class['IIDD'] < 0) & (diff_cohesion_decay_class['NDC'] < 0)]

    diff_cohesion_import_decay_class = diff_cohesion_decay_class[
        (diff_cohesion_decay_class['IODD'] < 0) & (diff_cohesion_decay_class['NOI'] < 0) |
        (diff_cohesion_decay_class['IIDD'] < 0) & (diff_cohesion_decay_class['NOID'] < 0)]

    diff_merge_class_and_method = pd.merge(diff_method_measure, diff_cohesion_decay_class, on='class_name')
    diff_cohesion_call_decay_class = diff_merge_class_and_method[
        (diff_merge_class_and_method['IODD'] < 0) & (diff_merge_class_and_method['CBM'] < 0) & (
                diff_merge_class_and_method['IDMC'] < 0) & (diff_merge_class_and_method['m_FAN_OUT'] < 0) |
        (diff_merge_class_and_method['IIDD'] < 0) & (diff_merge_class_and_method['CBM'] < 0) & (
                diff_merge_class_and_method['IDMC'] < 0) & (diff_merge_class_and_method['m_FAN_IN'] < 0)]

    return set_root_cause(diff_cohesion_import_decay_class, diff_cohesion_inherit_decay_class,
                          diff_cohesion_call_decay_class, opt, 'cohesion')


def set_root_cause(diff_import_decay_class, diff_inherit_decay_class, diff_call_decay_class, opt, problem):
    if problem == 'coupling':
        module_metric = 'scop'
    else:
        module_metric = 'scoh'
    diff_import_decay_class = diff_import_decay_class.reindex(
        columns=['root cause', 'module_name', module_metric, 'class_name', 'CBC'], fill_value='import')
    diff_inherit_decay_class = diff_inherit_decay_class.reindex(
        columns=['root cause', 'module_name', module_metric, 'class_name', 'CBC'], fill_value='inherit')
    if opt == 'extension':
        diff_call_decay_class = diff_call_decay_class.reindex(
            columns=['root cause', 'module_name', module_metric, 'class_name', 'CBC', 'method_name', 'CBM', 'startLine', 'ownership'],
            fill_value='call')
    else:
        diff_call_decay_class = diff_call_decay_class.reindex(
            columns=['root cause', 'module_name', module_metric, 'class_name', 'CBC', 'method_name', 'CBM', 'startLine'],
            fill_value='call')

    coupling_df = pd.concat([diff_call_decay_class, diff_inherit_decay_class,
                             diff_import_decay_class], axis=0)
    coupling_df.insert(0, 'problem', problem)
    return coupling_df
