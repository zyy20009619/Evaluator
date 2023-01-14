import os
import csv
from util.json_operator import read_folder, write_result_to_json
from util.path_operator import create_file_path
# from detect_algo.arch_debt.regression_model.model_selector import model_selector
from score_compete.index_measure import get_score
from util.metrics import MODULE_METRICS
from util.csv_operator import write_to_csv, write_to_one_line
import numpy as np


def analyse_data(diff_folder_path, output, obj):
    measure_diff, dep_diff = read_folder(diff_folder_path, 'measure_diff.json', 'dep_diff.json')
    if not (measure_diff or dep_diff):
        return False
    _scan_problems(diff_folder_path, measure_diff, dep_diff, output, obj)
    return True


def _scan_problems(diff_folder_path, measure_diff, dep_diff, output, obj):
    all_causes = dict()
    # 计算module
    # coupling_dic = dict()
    # functionality_list = list()
    # modularity_list = list()
    # evolution_list = list()
    # sort_dic = dict()
    causes_to_entities = list()
    # 构造变化趋势数组，计算综合评分，取综合评分最坏的top10定位问题
    change_list = list()
    module_name = list()
    for diff_module_name in measure_diff:
        change_list.append([measure_diff[diff_module_name]['scoh'], measure_diff[diff_module_name]['scop'],
                            measure_diff[diff_module_name]['odd'], measure_diff[diff_module_name]['idd'],
                            measure_diff[diff_module_name]['spread'], measure_diff[diff_module_name]['focus'],
                            measure_diff[diff_module_name]['icf'], measure_diff[diff_module_name]['ecf'],
                            measure_diff[diff_module_name]['rei'], measure_diff[diff_module_name]['DSM']])
        module_name.append(diff_module_name)
    [normalized_result, score_result] = get_score(change_list,
                                                  [[0.125], [0.125], [0.125], [0.125], [0.125], [0.125], [0.125],
                                                   [0.125], [0.125], [0.125]],
                                                  MODULE_METRICS)
    module_score = np.array(list(zip(module_name, score_result)))
    module_score = module_score[np.lexsort(module_score.T)]
    # write_to_csv(module_score.tolist(), create_file_path(output + '\\analyseResult', 'score.csv'))
    # all_causes['score'] = module_score.tolist()
    cause_list = list()  # 放置由伴生->伴生 or  伴生->原生引起的质量变差实体
    if obj == 'aosp':
        cause_list.append(
            ['module_name', 'score', 'ranking', 'phenomenon', 'src', 'src_no_aosp', 'dest', 'dest_no_aosp', 'type'])
    else:
        cause_list.append(['module_name', 'score', 'ranking', 'phenomenon', 'src', 'dest', 'type'])
    index = 1
    for item in module_score:
        diff_module_name = item[0]
        # find functionality problems at the class-level
        _find_causes_at_functionality(measure_diff[diff_module_name]['classes'], causes_to_entities)
        phenomenons = dict()
        no_aosp = dict()
        if obj == 'aosp':
            # 先读取项目中所有实体以及其对应的数据类型，然后为每条问题依赖扫描是伴生对伴生的依赖 or 原生对原生依赖 or 伴生对伴生依赖
            reader = csv.DictReader(open(os.path.join(output, 'final_ownership.csv')))
            for row in reader:
                no_aosp[row['qualifiedName']] = row['not_aosp']
        if float(measure_diff[diff_module_name]['scoh']) < 0:
            phenomenon = 'Violation of the high cohesion principle(scoh declining)'
            phenomenons[phenomenon] = _find_low_cohesion_causes(
                measure_diff[diff_module_name], dep_diff, no_aosp, phenomenon, cause_list, item, index, causes_to_entities)
        if float(measure_diff[diff_module_name]['scop']) > 0:
            phenomenon = 'Violation of low coupling principle (scop rising)'
            phenomenons[phenomenon] = _find_high_coupling_causes(measure_diff[diff_module_name], dep_diff, no_aosp,
                                                                 phenomenon, cause_list, item, index, causes_to_entities)
        if float(measure_diff[diff_module_name]['rei']) > 0:
            phenomenon = 'Violation of evolutionary principle (rei rising)'
            phenomenons[phenomenon] = _find_low_evolvability_causes(measure_diff[diff_module_name], no_aosp, phenomenon,
                                                                    cause_list)
        all_causes[diff_module_name] = phenomenons
        # # problem2: δscop>0
        # if float(measure_diff[diff_module_name]['scop']) > 0:
        #     # root cause1: the number of coupling ↑
        #     is_coupling_num = False
        #     if float(measure_diff[diff_module_name]['odd']) > 0 or float(measure_diff[diff_module_name]['idd']) > 0:
        #         is_coupling_num = True
        #     inherit_entities, call_entities, import_entities = _scan_causes_at_class(
        #         measure_diff[diff_module_name]['classes'], dep_diff,
        #         causes_entities, causes_to_entities)
        #     coupling_dic[diff_module_name] = {'the number of coupling modules increases': is_coupling_num,
        #                                       'inherit': inherit_entities, 'call': call_entities,
        #                                       'import': import_entities}
        #     sort_dic[diff_module_name] = float(measure_diff[diff_module_name]['scop'])
        index = index + 1
    # sort coupling_dic by scop
    # coupling_dic = _sort_coupling_dic(coupling_dic, sort_dic)
    # all_causes['coupling'] = coupling_dic
    # all_causes['functionality'] = functionality_list
    # all_causes['modularity'] = modularity_list
    # all_causes['evolution'] = evolution_list
    write_to_csv(cause_list, create_file_path(output + '\\analyseResult', 'causes.csv'))
    write_to_one_line(causes_to_entities, create_file_path(output + '\\analyseResult', 'causes_entities.csv'))
    write_result_to_json(create_file_path(output + '\\analyseResult', 'causes.json'), all_causes)


def _find_low_cohesion_causes(diff_module, dep_diff, no_aosp, phenomenon, cause_list, item, index, causes_to_entities):
    causes = dict()
    count = 1
    if diff_module['DSM'] > 0:
        causes['cause' + str(++count)] = 'Increasing in module size'
    _scan_causes_of_cohesion(diff_module['classes'], dep_diff, causes, count, no_aosp, phenomenon, cause_list, item,
                             index, causes_to_entities)
    return causes


def _find_high_coupling_causes(diff_module, dep_diff, no_aosp, phenomenon, cause_list, item, index, causes_to_entities):
    causes = dict()
    count = 1
    if diff_module['DSM'] > 0:
        causes['cause' + str(++count)] = 'Increasing in module size'
    if diff_module['idd'] > 0:
        causes['cause' + str(++count)] = 'Dependenced degree increasely on external modules'
    if diff_module['odd'] > 0:
        causes['cause' + str(++count)] = 'Increase of dependence on external modules'
    _scan_causes_of_coupling(diff_module['classes'], dep_diff, causes, count, no_aosp, phenomenon, cause_list, item,
                             index, causes_to_entities)
    return causes


def _find_low_evolvability_causes(diff_module, no_aosp, phenomenon, cause_list):
    causes = dict()
    count = 1
    if diff_module['icf'] < 0:
        if diff_module['DSM'] > 0:
            causes['cause' + str(
                ++count)] = 'Increasing size of module leads to the decrease of co-evolution in this module'
        else:
            causes['cause' + str(++count)] = 'Decreasing degree of co-evolution in this module'
    if diff_module['ecf'] > 0:
        causes['cause' + str(++count)] = 'Increasing degree of co-evolution among modules'
    return causes


def _sort_coupling_dic(coupling_dic, sort_dic):
    sorted_coupling_dic = dict()
    sort_dic_tuple = sorted(sort_dic.items(), key=lambda x: x[1], reverse=True)
    for tuple in sort_dic_tuple:
        sorted_coupling_dic[tuple[0]] = coupling_dic[tuple[0]]
    return sorted_coupling_dic


def _find_causes_at_functionality(classes_dic, causes_to_entities):
    for class_name in classes_dic:
        if float(classes_dic[class_name]['c_chm']) < 0 and float(classes_dic[class_name]['c_chd']) < 0:
            causes_to_entities.append(['functionality', class_name])


def _scan_causes_of_cohesion(classes_dic, dep_diff, causes, count, no_aosp, phenomenon, cause_list, item, index, causes_to_entities):
    for class_name in classes_dic:
        inherit_entities = list()
        import_entities = list()
        call_entities = list()
        if 'cause2' not in causes:
            causes['cause2'] = dict()
            causes['cause2']['cause'] = 'Decreasing number of dependency'
        if classes_dic[class_name]['IDCC'] < 0:
            # root cause1: by inherit
            if classes_dic[class_name]['IODD'] < 0 and classes_dic[class_name]['NAC'] < 0:
                if class_name in dep_diff['inherit']:
                    inherit_entities.append(
                        {'src': class_name, 'dest': dep_diff['inherit'][class_name], 'type': 'inherit'})
                    if type(dep_diff['inherit'][class_name][0]) == dict:
                        dest_name = dep_diff['inherit'][class_name][0]['name']
                    else:
                        dest_name = dep_diff['inherit'][class_name][0]
                    if class_name not in no_aosp:
                        cause_list.append([item[0], item[1], index, phenomenon, class_name, dest_name, 'inherit'])
                    elif dest_name in no_aosp and not (no_aosp[class_name] == '0' and no_aosp[dest_name] == '0'):
                        cause_list.append(
                            [item[0], item[1], index, phenomenon, class_name, no_aosp[class_name],
                             dest_name, no_aosp[dest_name], 'inherit'])
                    # if 'cohesion' not in causes_to_entities:
                    #     causes_to_entities['cohesion'] = list()
                    causes_to_entities.append(['cohesion', class_name])
            if classes_dic[class_name]['IIDD'] < 0 and classes_dic[class_name]['NDC'] < 0:
                if class_name in dep_diff['descendent']:
                    inherit_entities.append(
                        {'src': class_name, 'dest': dep_diff['descendent'][class_name], 'type': 'descendent'})
                    if type(dep_diff['descendent'][class_name][0]) == dict:
                        dest_name = dep_diff['descendent'][class_name][0]['name']
                    else:
                        dest_name = dep_diff['descendent'][class_name][0]
                    if class_name not in no_aosp:
                        cause_list.append([item[0], item[1], index, phenomenon, class_name, dest_name, 'descendent'])
                    elif dest_name in no_aosp and  not (no_aosp[class_name] == '0' and no_aosp[dest_name] == '0'):
                        cause_list.append(
                            [item[0], item[1], index, phenomenon, class_name, no_aosp[class_name],
                             dest_name,
                             no_aosp[dest_name], 'descendent'])
                    # causes_entities.append(class_name)
                    # if 'cohesion' not in causes_to_entities:
                    #     causes_to_entities['cohesion'] = list()
                    causes_to_entities.append(['cohesion', class_name])
            if len(inherit_entities) != 0:
                if class_name not in causes['cause2']:
                    causes['cause2'][class_name] = dict()
                causes['cause2'][class_name][
                    'Decreasing number of inherit dependency in this module'] = inherit_entities

            # root cause2: by import
            if classes_dic[class_name]['IODD'] < 0 and classes_dic[class_name]['NOI'] < 0:
                if class_name in dep_diff['import']:
                    import_entities.append(
                        {'src': class_name, 'dest': dep_diff['import'][class_name], 'type': 'import'})
                    if type(dep_diff['import'][class_name][0]) == dict:
                        dest_name = dep_diff['import'][class_name][0]['name']
                    else:
                        dest_name = dep_diff['import'][class_name][0]
                    if class_name not in no_aosp:
                        cause_list.append([item[0], item[1], index, phenomenon, class_name, dest_name, 'import'])
                    elif dest_name in no_aosp and  not (no_aosp[class_name] == '0' and no_aosp[dest_name] == '0'):
                        cause_list.append(
                    [item[0], item[1], index, phenomenon, class_name, no_aosp[class_name],
                     dest_name,no_aosp[dest_name], 'import'])
                    # causes_entities.append(class_name)
                    # if 'cohesion' not in causes_to_entities:
                    #     causes_to_entities['cohesion'] = list()
                    causes_to_entities.append(['cohesion', class_name])
            if classes_dic[class_name]['IIDD'] < 0 and classes_dic[class_name]['NOID'] < 0:
                if class_name in dep_diff['imported']:
                    import_entities.append(
                {'src': class_name, 'dest': dep_diff['imported'][class_name], 'type': 'imported'})
                    if type(dep_diff['imported'][class_name][0]) == dict:
                        dest_name = dep_diff['imported'][class_name][0]['name']
                    else:
                        dest_name = dep_diff['imported'][class_name][0]
                    if class_name not in no_aosp:
                        cause_list.append([item[0], item[1], index, phenomenon, class_name, dest_name, 'imported'])
                    elif dest_name in no_aosp and  not (no_aosp[class_name] == '0' and no_aosp[dest_name] == '0'):
                        cause_list.append(
                    [item[0], item[1], index, phenomenon, class_name, no_aosp[class_name],
                     dest_name, no_aosp[dest_name], 'imported'])
                    # causes_entities.append(class_name)
                    # if 'cohesion' not in causes_to_entities:
                    #     causes_to_entities['cohesion'] = list()
                    causes_to_entities.append(['cohesion', class_name])
            if len(import_entities) != 0:
                if class_name not in causes['cause2']:
                    causes['cause2'][class_name] = dict()
                    causes['cause2'][class_name][
                    'Decreasing number of import dependency in this module'] = import_entities

            # root cause3: by method invoke
            for method_name in classes_dic[class_name]['methods']:
                if classes_dic[class_name]['IODD'] < 0 and classes_dic[class_name]['methods'][method_name]['CBM'] < 0 and classes_dic[class_name]['methods'][method_name]['EDMC'] < 0 and classes_dic[class_name]['methods'][method_name]['m_FAN_OUT'] < 0:
                    if method_name in dep_diff['call']:
                        call_entities.append(
                    {'src': method_name, 'dest': dep_diff['call'][method_name], 'type': 'call'})
                        if type(dep_diff['call'][class_name][0]) == dict:
                            dest_name = dep_diff['call'][class_name][0]['name']
                        else:
                            dest_name = dep_diff['call'][class_name][0]
                        if class_name not in no_aosp:
                            cause_list.append(
                                [item[0], item[1], index, phenomenon, class_name, dest_name, 'call'])
                        elif dest_name in no_aosp and  not (no_aosp[class_name] == '0' and no_aosp[dest_name] == '0'):
                            cause_list.append([item[0], item[1], index, phenomenon, class_name, no_aosp[class_name],
                         dest_name, no_aosp[dest_name], 'call'])
                        # causes_entities.append(class_name)
                        # if 'cohesion' not in causes_to_entities:
                        #     causes_to_entities['cohesion'] = list()
                        causes_to_entities.append(['cohesion', class_name])
                if classes_dic[class_name]['IIDD'] < 0 and classes_dic[class_name]['c_FAN_IN'] < 0 and \
                        classes_dic[class_name]['methods'][method_name]['CBM'] < 0 and \
                        classes_dic[class_name]['methods'][method_name]['EDMC'] < 0 and \
                        classes_dic[class_name]['methods'][method_name]['m_FAN_IN'] < 0:
                    if method_name in dep_diff["called"]:
                        call_entities.append(
                    {'src': method_name, 'dest': dep_diff['called'][method_name], 'type': 'called'})
                        if type(dep_diff['called'][class_name][0]) == dict:
                            dest_name = dep_diff['called'][class_name][0]['name']
                        else:
                            dest_name = dep_diff['called'][class_name][0]
                        if class_name not in no_aosp:
                            cause_list.append(
                                [item[0], item[1], index, phenomenon, class_name, dest_name, 'called'])
                        elif dest_name in no_aosp and  not (no_aosp[class_name] == '0' and no_aosp[dest_name] == '0'):
                            cause_list.append(
                        [item[0], item[1], index, phenomenon, class_name, no_aosp[class_name],
                         dest_name,
                         no_aosp[dest_name], 'called'])
                        # causes_entities.append(class_name)
                        # if 'cohesion' not in causes_to_entities:
                        #     causes_to_entities['cohesion'] = list()
                        causes_to_entities.append(['cohesion', class_name])
            if len(call_entities) != 0:
                if class_name not in causes['cause2']:
                    causes['cause2'][class_name] = dict()
                    causes['cause2'][class_name]['Decreasing number of call dependency in this module'] = call_entities


def _scan_causes_of_coupling(classes_dic, dep_diff, causes, count, no_aosp, phenomenon, cause_list, item, index, causes_to_entities):
    for class_name in classes_dic:
        inherit_entities = list()
        import_entities = list()
        call_entities = list()
        if 'cause2' not in causes:
            causes['cause2'] = dict()
            causes['cause2']['cause'] = 'Decreasing number of dependency'
        if classes_dic[class_name]['CBC'] > 0 and classes_dic[class_name]['EDCC'] > 0.3 * classes_dic[class_name]['CBC']:
            # root cause1: by inherit
            if classes_dic[class_name]['c_FAN_OUT'] > 0 and classes_dic[class_name]['NAC'] > 0:
                if class_name in dep_diff['inherit']:
                    inherit_entities.append(
                        {'src': class_name, 'dest': dep_diff['inherit'][class_name], 'type': 'inherit'})
                    if type(dep_diff['inherit'][class_name][0]) == dict:
                        dest_name = dep_diff['inherit'][class_name][0]['name']
                    else:
                        dest_name = dep_diff['inherit'][class_name][0]
                    if class_name not in no_aosp:
                        cause_list.append([item[0], item[1], index, phenomenon, class_name, dest_name, 'inherit'])
                    elif dest_name in no_aosp and  not (no_aosp[class_name] == '0' and no_aosp[dest_name] == '0'):
                        cause_list.append(
                            [item[0], item[1], index, phenomenon, class_name, no_aosp[class_name],
                             dest_name, no_aosp[dest_name],
                             'inherit'])
                    # if 'coupling' not in causes_to_entities:
                    #     causes_to_entities['coupling'] = list()
                    causes_to_entities.append(['coupling', class_name])
            if classes_dic[class_name]['c_FAN_IN'] > 0 and classes_dic[class_name]['NDC'] > 0:
                if class_name in dep_diff['descendent']:
                    inherit_entities.append(
                        {'src': class_name, 'dest': dep_diff['descendent'][class_name], 'type': 'descendent'})
                    if type(dep_diff['descendent'][class_name][0]) == dict:
                        dest_name = dep_diff['descendent'][class_name][0]['name']
                    else:
                        dest_name = dep_diff['descendent'][class_name][0]
                    if class_name not in no_aosp:
                        cause_list.append([item[0], item[1], index, phenomenon, class_name, dest_name, 'descendent'])
                    elif dest_name in no_aosp and not (no_aosp[class_name] == '0' and no_aosp[dest_name] == '0'):
                        cause_list.append(
                            [item[0], item[1], index, phenomenon, class_name, no_aosp[class_name],
                             dest_name, no_aosp[dest_name],
                             'descendent'])
                    # if 'coupling' not in causes_to_entities:
                    #     causes_to_entities['coupling'] = list()
                    causes_to_entities.append(['coupling', class_name])
            if len(inherit_entities) != 0:
                if class_name not in causes['cause2']:
                    causes['cause2'][class_name] = dict()
                causes['cause2'][class_name]['Increasing number of inherit dependency in this class'] = inherit_entities

            # root cause2: by import
            if classes_dic[class_name]['c_FAN_OUT'] > 0 and classes_dic[class_name]['NOI'] > 0:
                if class_name in dep_diff['import']:
                    import_entities.append(
                        {'src': class_name, 'dest': dep_diff['import'][class_name], 'type': 'import'})
                    if type(dep_diff['import'][class_name][0]) == dict:
                        dest_name = dep_diff['import'][class_name][0]['name']
                    else:
                        dest_name = dep_diff['import'][class_name][0]
                    if class_name not in no_aosp:
                        cause_list.append([item[0], item[1], index, phenomenon, class_name, dest_name, 'import'])
                    elif dest_name in no_aosp and  not (no_aosp[class_name] == '0' and no_aosp[dest_name] == '0'):
                        cause_list.append(
                            [item[0], item[1], index, phenomenon, class_name, no_aosp[class_name],
                             dest_name, no_aosp[dest_name],
                             'import'])
                    # if 'coupling' not in causes_to_entities:
                    #     causes_to_entities['coupling'] = list()
                    causes_to_entities.append(['coupling', class_name])
            if classes_dic[class_name]['c_FAN_IN'] > 0 and classes_dic[class_name]['NOID'] > 0:
                if class_name in dep_diff['imported']:
                    import_entities.append(
                        {'src': class_name, 'dest': dep_diff['imported'][class_name], 'type': 'imported'})
                    if type(dep_diff['imported'][class_name][0]) == dict:
                        dest_name = dep_diff['imported'][class_name][0]['name']
                    else:
                        dest_name = dep_diff['imported'][class_name][0]
                    if class_name not in no_aosp:
                        cause_list.append([item[0], item[1], index, phenomenon, class_name, dest_name, 'imported'])
                    elif dest_name in no_aosp and  not (no_aosp[class_name] == '0' and no_aosp[dest_name] == '0'):
                        cause_list.append(
                            [item[0], item[1], index, phenomenon, class_name, no_aosp[class_name],
                             dest_name, no_aosp[dest_name],
                             'imported'])
                    # if 'coupling' not in causes_to_entities:
                    #     causes_to_entities['coupling'] = list()
                    causes_to_entities.append(['coupling', class_name])
            if len(import_entities) != 0:
                if class_name not in causes['cause2']:
                    causes['cause2'][class_name] = dict()
                causes['cause2'][class_name]['Increasing number of import dependency in this class'] = import_entities

            # root cause3: by method invoke
            for method_name in classes_dic[class_name]['methods']:
                if classes_dic[class_name]['c_FAN_OUT'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['CBM'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['EDMC'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['m_FAN_OUT'] > 0:
                    if method_name in dep_diff['call']:
                        call_entities.append(
                            {'src': method_name, 'dest': dep_diff['call'][method_name], 'type': 'call'})
                        if type(dep_diff['call'][class_name][0]) == dict:
                            dest_name = dep_diff['call'][class_name][0]['name']
                        else:
                            dest_name = dep_diff['call'][class_name][0]
                        if class_name not in no_aosp:
                            cause_list.append([item[0], item[1], index, phenomenon, class_name, dest_name, 'call'])
                        elif dest_name in no_aosp and  not (no_aosp[class_name] == '0' and no_aosp[dest_name] == '0'):
                            cause_list.append(
                                [item[0], item[1], index, phenomenon, class_name, no_aosp[class_name],
                                 dest_name, no_aosp[dest_name],
                                 'call'])
                        # if 'coupling' not in causes_to_entities:
                        #     causes_to_entities['coupling'] = list()
                        causes_to_entities.append(['coupling', class_name])
                if classes_dic[class_name]['c_FAN_IN'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['CBM'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['EDMC'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['m_FAN_IN'] > 0:
                    if method_name in dep_diff["called"]:
                        call_entities.append(
                            {'src': method_name, 'dest': dep_diff['called'][method_name], 'type': 'called'})
                        if type(dep_diff['called'][class_name][0]) == dict:
                            dest_name = dep_diff['called'][class_name][0]['name']
                        else:
                            dest_name = dep_diff['called'][class_name][0]
                        if class_name not in no_aosp:
                            cause_list.append([item[0], item[1], index, phenomenon, class_name, dest_name, 'called'])
                        elif dest_name in no_aosp and not (no_aosp[class_name] == '0' and no_aosp[dest_name] == '0'):
                            cause_list.append(
                                [item[0], item[1], index, phenomenon, class_name, no_aosp[class_name],
                                 dest_name, no_aosp[dest_name],
                                 'called'])
                        # if 'coupling' not in causes_to_entities:
                        #     causes_to_entities['coupling'] = list()
                        causes_to_entities.append(['coupling', class_name])
            if len(call_entities) != 0:
                if class_name not in causes['cause2']:
                    causes['cause2'][class_name] = dict()
                causes['cause2'][class_name]['Increasing number of call dependency in this class'] = call_entities

    return inherit_entities, call_entities, import_entities
