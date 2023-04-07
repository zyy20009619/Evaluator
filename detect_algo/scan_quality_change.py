import os
from util.csv_operator import read_csv_folder
from util.metrics import *
import pandas as pd
import numpy as np
from util.json_operator import *
from util.path_operator import create_file_path


# MODULE_METRICS.append('module_name')
# CLASS_METRICS.append('class_name')
# METHOD_METRICS.append('class_name')
# METHOD_METRICS.append('method_name')
# METHOD_METRICS = ['class_name', 'method_name', 'CBM', 'm_FAN_IN', 'm_FAN_OUT', 'IDMC', 'EDMC']


# 检测安卓扩展场景和一般场景腐化问题及根因
def detect_change(path1, path2, opt, th):
    base_out = create_file_path(os.path.join(path2, 'analyseResult' + str(th)), '')
    # 读取path1和path2数据
    class1_res, class2_res, method1_res, method2_res = read_csv_folder(
        os.path.join(path1, 'measure_result_class.csv'),
        os.path.join(path2, 'measure_result_class.csv'),
        os.path.join(path1, 'measure_result_method.csv'),
        os.path.join(path2, 'measure_result_method.csv'))
    dep1_res = pd.read_json(os.path.join(path1, 'dep.json'), encoding="utf-8", orient='records')
    dep1_res = dep1_res.transpose()
    dep2_res = pd.read_json(os.path.join(path2, 'dep.json'), encoding="utf-8", orient='records')
    dep2_res = dep2_res.transpose()
    diff_class_inner, diff_class_left, diff_class_right, diff_class_all = com_diff(class1_res, class2_res, base_out,
                                                                                   'module_name', 'class_name', 'class',
                                                                                   65)
    diff_method_inner, diff_method_left, diff_method_right, diff_method_all = com_diff(method1_res, method2_res,
                                                                                       base_out, 'class_name',
                                                                                       'method_name', 'method', 11)
    # 分别对扩展场景和一般场景进行不同逻辑处理
    if opt == 'extension':
        # 读取耦合切面数据
        facade_data = read_file(os.path.join(path2, 'facade.json'))
        # 安卓场景下关注伴生相对于原生进行修改的类实体是否引起较大的腐化
        res = detect_android_project(base_out, facade_data, class2_res, diff_class_inner, diff_method_all, opt, th)
        # 统计检测结果数据
        intrusive_coupling_call_class = len(
            set(res[(res['class_ownership'] == 'intrusive native') & (res['problem'] == 'coupling') & (
                    res['root cause'] == 'call')]['problem class']))
        intrusive_coupling_inherit_class = len(
            set(res[(res['class_ownership'] == 'intrusive native') & (res['problem'] == 'coupling') & (
                    res['root cause'] == 'inherit')]['problem class']))
        intrusive_coupling_import_class = len(
            set(res[(res['class_ownership'] == 'intrusive native') & (res['problem'] == 'coupling') & (
                    res['root cause'] == 'import')]['problem class']))
        intrusive_coupling_call_method = len(
            set(res[(res['class_ownership'] == 'intrusive native') & (res['problem'] == 'coupling') & (
                    res['root cause'] == 'call')]['problem method']))
        intrusive_cohesion_call_class = len(
            set(res[(res['class_ownership'] == 'intrusive native') & (res['problem'] == 'cohesion') & (
                    res['root cause'] == 'call')]['problem class']))
        intrusive_cohesion_inherit_class = len(
            set(res[(res['class_ownership'] == 'intrusive native') & (res['problem'] == 'cohesion') & (
                    res['root cause'] == 'inherit')]['problem class']))
        intrusive_cohesion_import_class = len(
            set(res[(res['class_ownership'] == 'intrusive native') & (res['problem'] == 'cohesion') & (
                    res['root cause'] == 'import')]['problem class']))
        intrusive_cohesion_call_method = len(
            set(res[(res['class_ownership'] == 'intrusive native') & (res['problem'] == 'cohesion') & (
                    res['root cause'] == 'call')]['problem method']))
        actively_coupling_call_class = len(
            set(res[(res['class_ownership'] == 'actively native') & (res['problem'] == 'coupling') & (
                    res['root cause'] == 'call')]['problem class']))
        actively_coupling_inherit_class = len(
            set(res[(res['class_ownership'] == 'actively native') & (res['problem'] == 'coupling') & (
                    res['root cause'] == 'inherit')]['problem class']))
        actively_coupling_import_class = len(
            set(res[(res['class_ownership'] == 'actively native') & (res['problem'] == 'coupling') & (
                    res['root cause'] == 'import')]['problem class']))
        actively_coupling_call_method = len(
            set(res[(res['class_ownership'] == 'actively native') & (res['problem'] == 'coupling') & (
                    res['root cause'] == 'call')]['problem method']))
        actively_cohesion_call_class = len(
            set(res[(res['class_ownership'] == 'actively native') & (res['problem'] == 'cohesion') & (
                    res['root cause'] == 'call')]['problem class']))
        actively_cohesion_inherit_class = len(
            set(res[(res['class_ownership'] == 'actively native') & (res['problem'] == 'cohesion') & (
                    res['root cause'] == 'inherit')]['problem class']))
        actively_cohesion_import_class = len(
            set(res[(res['class_ownership'] == 'actively native') & (res['problem'] == 'cohesion') & (
                    res['root cause'] == 'import')]['problem class']))
        actively_cohesion_call_method = len(
            set(res[(res['class_ownership'] == 'actively native') & (res['problem'] == 'cohesion') & (
                    res['root cause'] == 'call')]['problem method']))
        intrusive_class = len(set(res[(res['class_ownership'] == 'intrusive native')]['problem class']))
        intrusive_method = len(set(res[(res['class_ownership'] == 'intrusive native')]['problem method']))
        actively_class = len(set(res[(res['class_ownership'] == 'actively native')]['problem class']))
        actively_method = len(set(res[(res['class_ownership'] == 'actively native')]['problem method']))
        count_pd = pd.DataFrame(data=[
            [intrusive_coupling_call_class, intrusive_coupling_inherit_class, intrusive_coupling_import_class,
             intrusive_coupling_call_method, intrusive_cohesion_call_class, intrusive_cohesion_inherit_class,
             intrusive_cohesion_import_class, intrusive_cohesion_call_method, actively_coupling_call_class,
             actively_coupling_inherit_class, actively_coupling_import_class, actively_coupling_call_method,
             actively_cohesion_call_class, actively_cohesion_inherit_class, actively_cohesion_import_class,
             actively_cohesion_call_method, intrusive_class, intrusive_method, actively_class, actively_method]],
            columns=['#intrusive-耦合问题类(call)', '#intrusive-耦合问题类(inherit)',
                     '#intrusive-耦合问题类(import)',
                     '#intrusive-耦合问题方法(call)', '#intrusive-内聚问题类(call)',
                     '#intrusive-内聚问题类(inherit)',
                     '#intrusive-内聚问题类(import)', '#intrusive-内聚问题方法(call)',
                     '#actively-耦合问题类(call)', '#actively-耦合问题类(inherit)', '#actively-耦合问题类(import)',
                     '#actively-耦合问题方法(call)', '#actively-内聚问题类(call)', '#actively-内聚问题类(inherit)',
                     '#actively-内聚问题类(import)', '#actively-内聚问题方法(call)',
                     '#intrusive-问题类', '#intrusive-问题方法', '#actively-问题类', '#actively-问题方法'])
    elif opt == 'sextension':
        # 读取耦合切面数据
        facade_data = read_file(os.path.join(path2, 'facade.json'))
        # 自身演化以package粒度去评估
        res = detect_common_project(diff_class_all, diff_method_all, opt, th)
        # 将检测结果依据归属方信息进行整理
    else:
        # 一般场景下关注新版本相对于旧版本在模块质量上是否发生较大腐化
        res, dep_res = detect_common_project(diff_class_all, diff_method_all, dep1_res, dep2_res, opt, th)
        write_result_to_json(os.path.join(base_out, "detection dep.json"), dep_res)
        # 统计检测结果数据
        res_count = [len(set(res[(res['problem'] == 'coupling') & (res['root cause'] == 'call')]['problem module'])),
                     len(set(res[(res['problem'] == 'coupling') & (res['root cause'] == 'inherit')]['problem module'])),
                     len(set(res[(res['problem'] == 'coupling') & (res['root cause'] == 'import')]['problem module'])),
                     len(set(res[(res['problem'] == 'coupling') & (res['root cause'] == 'call')]['problem class'])),
                     len(set(res[(res['problem'] == 'coupling') & (res['root cause'] == 'inherit')]['problem class'])),
                     len(set(res[(res['problem'] == 'coupling') & (res['root cause'] == 'import')]['problem class'])),
                     len(set(res[(res['problem'] == 'coupling') & (res['root cause'] == 'call')]['problem method'])),
                     len(set(res[(res['problem'] == 'cohesion') & (res['root cause'] == 'call')]['problem module'])),
                     len(set(res[(res['problem'] == 'cohesion') & (res['root cause'] == 'inherit')]['problem module'])),
                     len(set(res[(res['problem'] == 'cohesion') & (res['root cause'] == 'import')]['problem module'])),
                     len(set(res[(res['problem'] == 'cohesion') & (res['root cause'] == 'call')]['problem class'])),
                     len(set(res[(res['problem'] == 'cohesion') & (res['root cause'] == 'inherit')]['problem class'])),
                     len(set(res[(res['problem'] == 'cohesion') & (res['root cause'] == 'import')]['problem class'])),
                     len(set(res[(res['problem'] == 'cohesion') & (res['root cause'] == 'call')]['problem method'])),
                     len(set(res['problem module'])), len(set(res['problem class'])), len(set(res['problem method']))]
        count_pd = pd.DataFrame(data=[res_count],
                                columns=['#耦合问题模块(call)', '#耦合问题模块(inherit)', '#耦合问题模块(import)',
                                         '#耦合问题类(call)', '#耦合问题类(inherit)', '#耦合问题类(import)', '#耦合问题方法(call)',
                                         '#内聚问题模块(call)', '#内聚问题模块(inherit)', '#内聚问题模块(import)',
                                         '#内聚问题类(call)', '#内聚问题类(inherit)', '#内聚问题类(import)', '#内聚问题方法(call)',
                                         '#问题模块', '#问题类', '#问题方法'])
    res.to_csv(os.path.join(base_out, "detection result.csv"), index=False, sep=',')
    count_pd.to_csv(os.path.join(base_out, "detection count.csv"), index=False, sep=',')


def com_diff(res1, res2, base_out, focus_name1, focus_name2, grau, metric_num):
    # 获取到所有粒度实体的质量diff，diff包含三种状态：add/modify/delete
    # 求两个版本之间的实体交集/差集(df1-df2 & df2-df1)
    merge_inner = pd.merge(res1, res2,
                           how='inner', left_on=[focus_name2],
                           right_on=[focus_name2], suffixes=['1', ''])
    name_list = [focus_name1, focus_name2, 'filepath']
    drop_name_list = [focus_name1, focus_name1 + '1', focus_name2, 'filepath', 'filepath1']
    if grau == 'method':
        name_list = [focus_name1, focus_name2, 'startLine']
        drop_name_list = [focus_name1, focus_name1 + '1', focus_name2, 'filepath', 'filepath1', 'startLine',
                          'startLine1', 'module_name',
                          'module_name1']
    merge_inner_name = merge_inner[name_list]
    diff_inner = merge_inner.drop(drop_name_list, axis=1).diff(periods=metric_num, axis=1).iloc[
                 :, metric_num:]
    diff_inner = pd.concat([merge_inner_name, diff_inner], axis=1)
    diff_inner['status'] = 'modify'

    diff_left = pd.merge(res1, res2, how='left', left_on=[focus_name2], right_on=[focus_name2],
                         suffixes=['', '1'])
    # 如果包含非数字列，加入.select_dtypes(include=[np.number])
    diff_left = diff_left[diff_left.isna().any(axis=1)].dropna(axis=1, how='all')
    diff_left_name = diff_left if diff_left.empty else diff_left[[focus_name1, focus_name2]]
    # diff_left_name = diff_left[[focus_name1, focus_name2]]
    diff_left = -diff_left.select_dtypes(include=[np.number])
    diff_left = pd.concat([diff_left_name, diff_left], axis=1)
    diff_left['status'] = 'delete'

    diff_right = pd.merge(res1, res2, how='right', left_on=[focus_name2], right_on=[focus_name2],
                          suffixes=['1', ''])
    diff_right = diff_right[diff_right.isna().any(axis=1)].dropna(axis=1, how='all')
    diff_right['status'] = 'add'

    diff_all = pd.concat([diff_inner, diff_left, diff_right], axis=0).reset_index(drop=True)
    # del diff_all['module_name']
    # 输出所有class diff信息
    diff_all.to_csv(os.path.join(base_out, 'diff ' + grau + '.csv'), index=False, sep=',')

    return diff_inner, diff_left, diff_right, diff_all


def detect_android_project(base_out, facade_data, class2_res, diff_class, diff_method, opt, th):
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
    intrusive_res_pd = get_android_decay_root_cause(entity_pd, 'intrusive native', class2_res, diff_class, base_out,
                                                    diff_method, opt, th)
    actively_res_pd = get_android_decay_root_cause(entity_pd, 'actively native', class2_res, diff_class, base_out,
                                                   diff_method, opt,
                                                   th)
    extensive_res_pd = get_android_decay_root_cause(entity_pd, 'extensive', class2_res, diff_class, base_out,
                                                    diff_method, opt,
                                                    th)
    obsoletely_res_pd = get_android_decay_root_cause(entity_pd, 'obsoletely native', class2_res, diff_class, base_out,
                                                     diff_method, opt,
                                                     th)
    res_pd = pd.concat([intrusive_res_pd, actively_res_pd, extensive_res_pd, obsoletely_res_pd], axis=0)
    # res_pd = pd.concat([intrusive_res_pd], axis=0)
    res_pd = res_pd.rename(
        columns={'CBC': 'class decay degree', 'CBM': 'method decay degree', 'ownership': 'method_ownership',
                 'class_name': 'problem class', 'method_name': 'problem method'})
    return res_pd


def detect_common_project(diff_class_all, diff_method_all, dep1_res, dep2_res, opt, th):
    diff_module_modify = diff_class_all
    # 对新增或着删除的module不关注（即其中所有的类status都为add或delete）
    deleted_module = list()
    for name, group in diff_class_all.groupby('module_name'):
        if all((group['status'] == 'add') | (group['status'] == 'delete')):
            deleted_module.append(name)
    deleted_index = diff_module_modify[diff_module_modify['module_name'].isin(deleted_module)].index
    diff_module_modify = diff_module_modify.drop(index=deleted_index)
    return get_common_decay_root_cause(diff_module_modify, diff_method_all, dep1_res, dep2_res, opt, th)


def get_android_decay_root_cause(ownership_pd, ownership, class2_res, diff_class, base_out, diff_method, opt, th):
    ownership_class = ownership_pd[(ownership_pd['category'] == 'Class') & (ownership_pd['ownership'] == ownership)][
        'qualifiedName']
    if ownership != 'extensive':
        ownership_diff_class_measure = diff_class.loc[diff_class['class_name'].isin(ownership_class)]
        ownership_diff_class_measure.sort_values(by="CBC", inplace=True, ascending=False)
        # ownership_diff_class_measure.to_csv(os.path.join(base_out, 'diff ' + ownership + '.csv'), index=False, sep=',')
        # 对产生腐化的类实体进行定位（根据腐化严重程度进行输出）
        coupling_df = detect_coupling_problem(ownership_diff_class_measure, diff_method, opt, th)
        del coupling_df['scop']
        cohesion_df = detect_cohesion_problem(ownership_diff_class_measure, diff_method, opt)
        del cohesion_df['scoh']
        res_pd = pd.concat([coupling_df, cohesion_df], axis=0).reset_index(drop=True)
    else:
        class2_res.sort_values(by="CBC", inplace=True, ascending=False)
        class2_res = class2_res[class2_res['CBC'] > 0]
        res_pd = class2_res.loc[class2_res['class_name'].isin(ownership_class)][['module_name', 'class_name', 'CBC']]
        # res_pd = res_pd.rename(
        #     columns={'CBC': 'class decay degree','class_name': 'problem class', 'module_name': 'problem module'})

    res_pd.insert(0, 'class_ownership', ownership)
    return res_pd


def get_common_decay_root_cause(diff_module, diff_method, dep1_res, dep2_res, opt, th):
    dep_res = dict()
    # 对产生腐化的模块实体进行定位（根据腐化严重程度进行输出）
    diff_module.sort_values(by="scop", inplace=True, ascending=False)
    coupling_df = detect_coupling_problem(diff_module[diff_module['scop'] > 0], diff_method, opt, th)
    coupling_df = coupling_df.rename(
        columns={'scop': 'module decay degree'})
    coupling_res = dict()
    detect_root_dep(coupling_df, dep1_res, dep2_res, coupling_res)
    dep_res['coupling'] = coupling_res
    diff_module.sort_values(by="scoh", inplace=True, ascending=True)
    cohesion_df = detect_cohesion_problem(diff_module[diff_module['scoh'] < 0], diff_method, opt)
    cohesion_df = cohesion_df.rename(
        columns={'scoh': 'module decay degree'})
    cohesion_res = dict()
    detect_root_dep(cohesion_df, dep1_res, dep2_res, cohesion_res)
    dep_res['cohesion'] = cohesion_res
    res_pd = pd.concat([coupling_df, cohesion_df], axis=0)
    # 将module_name数据平移到module_name_y,将status数据平移到status_x，删除这两列
    res_pd = res_pd.rename(
        columns={'CBC': 'class decay degree', 'CBM': 'method decay degree',
                 'class_name': 'problem class', 'method_name': 'problem method',
                 'module_name': 'problem module'})
    return res_pd, dep_res


def detect_root_dep(pf_df, dep1, dep2, dep_res):
    # 定位call/import/inherit原因的依赖
    set_root_dep(pf_df[pf_df['root cause'] == 'call'], dep_res, dep1, dep2, 'call', 'called')
    set_root_dep(pf_df[pf_df['root cause'] == 'inherit'], dep_res, dep1, dep2, 'inherit', 'descendent')
    # set_root_dep(pf_df[pf_df['root cause'] == 'descendent'], dep_res, dep1, dep2, 'descendent')
    set_root_dep(pf_df[pf_df['root cause'] == 'import'], dep_res, dep1, dep2, 'import', 'imported')
    print('test')
    # set_root_dep(pf_df[pf_df['root cause'] == 'imported'], dep_res, dep1, dep2, 'imported')


def set_root_dep(pf_df, dep_res, dep1, dep2, dep_type, deped_type):
    # if dep_type == 'call':
    for index, row in pf_df.iterrows():
        if row[2] not in dep_res:
            dep_res[row[2]] = dict()
            dep_res[row[2]]['decay degree'] = round(row[3], 4)
            dep_res[row[2]]['root cause'] = dict()
        if dep_type not in dep_res[row[2]]['root cause']:
            dep_res[row[2]]['root cause'][dep_type] = dict()
        dep_res[row[2]]['root cause'][dep_type][row[4]] = dict()
        # dep_res[row[2]]['probelm class'][dep_type][row[4]]['decay degree'] = round(row[5], 4)
        dep_res[row[2]]['root cause'][dep_type][row[4]]['filepath'] = row[5]
        dep_res[row[2]]['root cause'][dep_type][row[4]]['status'] = row[7]
        dep_res[row[2]]['root cause'][dep_type][row[4]]['probelm dep'] = dict()

        if dep_type == 'call':
            if row[7] not in dep_res[row[2]]['root cause'][dep_type][row[4]]['probelm dep']:
                dep_res[row[2]]['root cause'][dep_type][row[4]]['probelm dep'][row[8]] = dict()
            # dep_res[row[2]]['probelm class'][dep_type][row[4]]['probelm dep'][row[7]]['decay degree'] = round(row[8], 4)
            dep_res[row[2]]['root cause'][dep_type][row[4]]['probelm dep'][row[8]]['startLine'] = row[10]
            dep_res[row[2]]['root cause'][dep_type][row[4]]['probelm dep'][row[8]]['status'] = row[11]
            # dep_res[row[2]]['probelm class'][dep_type][row[4]]['probelm dep'][row[7]]['probelm method'] = dict()
            method_dep_diff(row[11], row[2], row[4], row[8], dep_type, dep_res, dep1, dep2)
        else:
            class_dep_diff(row[7], row[2], row[4], dep_type, deped_type, dep_res, dep1, dep2)


def class_dep_diff(class_status, module_name, class_name, dep_type, deped_type, dep_res, dep1, dep2):
    if class_status == 'modify':
        type_dep1 = extr_class_dep(class_name, dep1, dep_type, deped_type)
        type_dep2 = extr_class_dep(class_name, dep2, dep_type, deped_type)
        inter_type_dep = type_dep1.keys() & type_dep2.keys()
        add_dep = type_dep2.keys() - inter_type_dep
        delete_dep = type_dep1.keys() - inter_type_dep
        if len(add_dep) != 0:
            add_tmp = dict()
            for ad in add_dep:
                add_tmp[ad] = type_dep2[ad]
            dep_res[module_name]['root cause'][dep_type][class_name]['probelm dep']['add'] = add_tmp
        if len(delete_dep) != 0:
            delete_tmp = dict()
            for dd in delete_dep:
                delete_tmp[dd] = type_dep1[dd]
            dep_res[module_name]['root cause'][dep_type][class_name]['probelm dep']['delete'] = delete_tmp
    elif class_status == 'add':
        add_dep = extr_class_dep(class_name, dep2, dep_type, deped_type)
        dep_res[module_name]['root cause'][dep_type][class_name]['probelm dep']['add'] = add_dep
    else:
        delete_dep = extr_class_dep(class_name, dep1, dep_type, deped_type)
        dep_res[module_name]['root cause'][dep_type][class_name]['probelm dep']['delete'] = delete_dep


def extr_class_dep(class_name, dep, dep_type, deped_type):
    type_dep = dict()
    if dep_type in dep.loc[class_name]['dep'] and type(dep.loc[class_name]['dep'][dep_type]) != float:
        type_dep = Merge(dep.loc[class_name]['dep'][dep_type], type_dep)
    if deped_type in dep.loc[class_name]['dep'] and type(dep.loc[class_name]['dep'][deped_type]) != float:
        type_dep = Merge(dep.loc[class_name]['dep'][deped_type], type_dep)
    return type_dep


def method_dep_diff(method_status, module_name, class_name, method_name, dep_type, dep_res, dep1, dep2):
    if method_name not in dep_res[module_name]['root cause'][dep_type][class_name]['probelm dep']:
        dep_res[module_name]['root cause'][dep_type][dep_type]['probelm dep'][method_name] = dict()
    if method_status == 'modify':
        type_dep1 = extr_method_dep(class_name, method_name, dep_type, dep1)
        type_dep2 = extr_method_dep(class_name, method_name, dep_type, dep2)
        inter_type_dep = type_dep1.keys() & type_dep2.keys()
        add_dep = type_dep2.keys() - inter_type_dep
        delete_dep = type_dep1.keys() - inter_type_dep
        if len(add_dep) != 0:
            add_tmp = dict()
            for ad in add_dep:
                add_tmp[ad] = type_dep2[ad]
            dep_res[module_name]['root cause'][dep_type][class_name]['probelm dep'][method_name]['add'] = add_tmp
        if len(delete_dep) != 0:
            delete_tmp = dict()
            for dd in delete_dep:
                delete_tmp[dd] = type_dep1[dd]
            dep_res[module_name]['root cause'][dep_type][class_name]['probelm dep'][method_name][
                'delete'] = delete_tmp
    elif method_status == 'add':
        add_dep = extr_method_dep(class_name, method_name, dep_type, dep2)
        if len(add_dep) != 0:
            dep_res[module_name]['root cause'][dep_type][class_name]['probelm dep'][method_name]['add'] = add_dep
    else:
        delete_dep = extr_method_dep(class_name, method_name, dep_type, dep1)
        if len(delete_dep) != 0:
            dep_res[module_name]['root cause'][dep_type][class_name]['probelm dep'][method_name][
                'delete'] = delete_dep


def extr_method_dep(class_name, method_name, dep_type, dep):
    type_dep = dict()
    if 'call' in dep.loc[class_name]['dep'] and type(dep.loc[class_name]['dep'][dep_type]) != float:
        if method_name in dep.loc[class_name]['dep'][dep_type]:
            type_dep = Merge(dep.loc[class_name]['dep'][dep_type][method_name], type_dep)
    if 'called' in dep.loc[class_name]['dep'] and type(dep.loc[class_name]['dep']['called']) != float:
        if method_name in dep.loc[class_name]['dep']['called']:
            type_dep = Merge(dep.loc[class_name]['dep']['called'][method_name], type_dep)
    return type_dep


def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def detect_coupling_problem(diff_class_measure, diff_method_measure, opt, th):
    # 规则集1：检测与外部的耦合情况
    diff_coupling_decay_class = diff_class_measure[
        (diff_class_measure['CBC'] > 0) & (diff_class_measure['EDCC'] > th * diff_class_measure['CBC'])]
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

    return set_root_cause(diff_coupling_import_decay_class, diff_coupling_inherit_decay_class,
                          diff_coupling_call_decay_class, opt, 'coupling')


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
        columns=['root cause', 'module_name', module_metric, 'class_name', 'filepath', 'CBC', 'status'],
        fill_value='import')
    diff_import_decay_class = diff_import_decay_class.rename(columns={'status': 'class status'})
    diff_inherit_decay_class = diff_inherit_decay_class.reindex(
        columns=['root cause', 'module_name', module_metric, 'class_name', 'filepath', 'CBC', 'status'],
        fill_value='inherit')
    diff_inherit_decay_class = diff_inherit_decay_class.rename(columns={'status': 'class status'})
    if opt == 'extension':
        diff_call_decay_class = diff_call_decay_class.reindex(
            columns=['root cause', 'module_name_y', module_metric, 'class_name', 'filepath', 'CBC', 'status_y',
                     'method_name',
                     'CBM', 'startLine',
                     'ownership', 'status_x'],
            fill_value='call')
    else:
        diff_call_decay_class = diff_call_decay_class.reindex(
            columns=['root cause', 'module_name_y', module_metric, 'class_name', 'filepath_y', 'CBC', 'status_y',
                     'method_name',
                     'CBM',
                     'startLine', 'status_x'],
            fill_value='call')
    diff_call_decay_class = diff_call_decay_class.rename(
        columns={'module_name_y': 'module_name', 'status_y': 'class status', 'status_x': 'method status', 'filepath_y': 'filepath'})
    problem_df = pd.concat([diff_call_decay_class, diff_inherit_decay_class,
                             diff_import_decay_class], axis=0)
    problem_df.insert(0, 'problem', problem)
    return problem_df
