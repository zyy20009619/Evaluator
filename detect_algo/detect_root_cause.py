import os
import matplotlib.pyplot as plt
from util.json_operator import read_folder, write_result_to_json
from util.path_operator import create_file_path
from detect_algo.arch_debt.measure_arch import measure_maintenance
from detect_algo.arch_debt.regression_model.model_selector import model_selector


def analyse_data(diff_folder_path, output):
    measure_diff, dep_diff = read_folder(diff_folder_path, 'measure_diff.json', 'dep_diff.json')
    if not (measure_diff or dep_diff):
        return False
    _scan_problems(diff_folder_path, measure_diff, dep_diff, output)
    return True


def _scan_problems(diff_folder_path, measure_diff, dep_diff, output):
    all_causes = dict()
    coupling_dic = dict()
    functionality_list = list()
    modularity_list = list()
    evolution_list = list()
    sort_dic = dict()
    causes_entities = list()
    causes_to_entities = dict()
    for diff_module_name in measure_diff:
        # problem1: find functionality problems at the class-level
        _find_causes_at_functionality(measure_diff[diff_module_name]['classes'], functionality_list, causes_entities,
                                      causes_to_entities)
        # problem2: δscop>0
        if float(measure_diff[diff_module_name]['scop']) > 0:
            # root cause1: the number of coupling ↑
            is_coupling_num = False
            if float(measure_diff[diff_module_name]['odd']) > 0 or float(measure_diff[diff_module_name]['idd']) > 0:
                is_coupling_num = True
            inherit_entities, call_entities, import_entities = _scan_causes_at_class(
                measure_diff[diff_module_name]['classes'], dep_diff,
                causes_entities, causes_to_entities)
            coupling_dic[diff_module_name] = {'the number of coupling modules increases': is_coupling_num,
                                              'inherit': inherit_entities, 'call': call_entities,
                                              'import': import_entities}
            sort_dic[diff_module_name] = float(measure_diff[diff_module_name]['scop'])
    # sort coupling_dic by scop
    coupling_dic = _sort_coupling_dic(coupling_dic, sort_dic)
    all_causes['coupling'] = coupling_dic
    all_causes['functionality'] = functionality_list
    all_causes['modularity'] = modularity_list
    all_causes['evolution'] = evolution_list
    write_result_to_json(create_file_path(output + '\\analyseResult', 'causes.json'), all_causes)


def _sort_coupling_dic(coupling_dic, sort_dic):
    sorted_coupling_dic = dict()
    sort_dic_tuple = sorted(sort_dic.items(), key=lambda x: x[1], reverse=True)
    for tuple in sort_dic_tuple:
        sorted_coupling_dic[tuple[0]] = coupling_dic[tuple[0]]
    return sorted_coupling_dic


def _find_causes_at_functionality(classes_dic, functionality_list, causes_entities, causes_to_entities):
    for class_name in classes_dic:
        if float(classes_dic[class_name]['c_chm']) < 0 and float(classes_dic[class_name]['c_chd']) < 0:
            functionality_list.append(class_name)
            causes_entities.append(class_name)
            if 'functionality' not in causes_to_entities:
                causes_to_entities['functionality'] = list()
            causes_to_entities['functionality'].append(class_name)


def _scan_causes_at_class(classes_dic, dep_diff, causes_entities, causes_to_entities):
    inherit_entities = list()
    import_entities = list()
    call_entities = list()
    for class_name in classes_dic:
        if classes_dic[class_name]['CBC'] > 0 and classes_dic[class_name]['EDCC'] > 0 and classes_dic[class_name]['IDCC'] <= 0:
            # root cause1: by inherit
            if classes_dic[class_name]['c_FAN_OUT'] > 0 and classes_dic[class_name]['NAC'] > 0:
                if class_name in dep_diff['inherit']:
                    inherit_entities.append(
                        {'src': class_name, 'dest': dep_diff['inherit'][class_name], 'type': 'inherit'})
                    causes_entities.append(class_name)
                    if 'coupling' not in causes_to_entities:
                        causes_to_entities['coupling'] = list()
                    causes_to_entities['coupling'].append(class_name)
            if classes_dic[class_name]['c_FAN_IN'] > 0 and classes_dic[class_name]['NDC'] > 0:
                if class_name in dep_diff['descendent']:
                    inherit_entities.append(
                        {'src': class_name, 'dest': dep_diff['descendent'][class_name], 'type': 'descendent'})
                    causes_entities.append(class_name)
                    if 'coupling' not in causes_to_entities:
                        causes_to_entities['coupling'] = list()
                    causes_to_entities['coupling'].append(class_name)

            # root cause2: by import
            if classes_dic[class_name]['EDCC'] > 0 and classes_dic[class_name]['c_FAN_OUT'] > 0 and \
                    classes_dic[class_name]['NOI'] > 0:
                if class_name in dep_diff['import']:
                    import_entities.append(
                        {'src': class_name, 'dest': dep_diff['import'][class_name], 'type': 'import'})
                    causes_entities.append(class_name)
                    if 'coupling' not in causes_to_entities:
                        causes_to_entities['coupling'] = list()
                    causes_to_entities['coupling'].append(class_name)
            if classes_dic[class_name]['EDCC'] > 0 and classes_dic[class_name]['c_FAN_OUT'] > 0 and \
                    classes_dic[class_name]['NOID'] > 0:
                if class_name in dep_diff['imported']:
                    import_entities.append(
                        {'src': class_name, 'dest': dep_diff['imported'][class_name], 'type': 'imported'})
                    causes_entities.append(class_name)
                    if 'coupling' not in causes_to_entities:
                        causes_to_entities['coupling'] = list()
                    causes_to_entities['coupling'].append(class_name)

            # root cause3: by method invoke
            for method_name in classes_dic[class_name]['methods']:
                if classes_dic[class_name]['EDCC'] > 0 and classes_dic[class_name]['c_FAN_OUT'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['CBM'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['EDMC'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['m_FAN_OUT'] > 0:
                    if method_name in dep_diff['call']:
                        call_entities.append(
                            {'src': method_name, 'dest': dep_diff['call'][method_name], 'type': 'call'})
                        causes_entities.append(class_name)
                        if 'coupling' not in causes_to_entities:
                            causes_to_entities['coupling'] = list()
                        causes_to_entities['coupling'].append(class_name)
                if classes_dic[class_name]['EDCC'] > 0 and classes_dic[class_name]['c_FAN_IN'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['CBM'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['EDMC'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['m_FAN_IN'] > 0:
                    if method_name in dep_diff["called"]:
                        call_entities.append(
                            {'src': method_name, 'dest': dep_diff['called'][method_name], 'type': 'called'})
                        causes_entities.append(class_name)
                        if 'coupling' not in causes_to_entities:
                            causes_to_entities['coupling'] = list()
                        causes_to_entities['coupling'].append(class_name)

    return inherit_entities, call_entities, import_entities
