import os
import matplotlib.pyplot as plt
import numpy as np
from module_measurement.module_metric_compete import get_module_metric
from analysis.indicate import gen_xlsx
from util.rel_data import get_rel_info
from util.csv_operator import write_result_to_csv
from util.json_operator import read_file, write_result_to_json, read_folder
from util.path_operator import create_file_path

GIT_COMMAND = 'git log  --pretty=format:"commit %H(%ad)%nauthor:%an%ndescription:%s"  --date=format:"%Y-%m-%d %H:%M:%S" --numstat  --name-status  --reverse  >./master.txt'

def measure_module_metrics(dep_path, output, mapping_path):
    dep_dic = read_file(dep_path)
    mapping_dic = read_file(mapping_path)
    if dep_dic and mapping_dic:
        module_info, method_class, call, called, dep, inherit, descendent, override, overrided, import_val, imported_val, parameter, method_define_var, method_use_field = get_rel_info(
            dep_dic, mapping_dic, output)
        module_dic = get_module_metric(dep_dic['variables'], module_info, inherit, descendent, method_class, dep, call,
                                       called, override, overrided, import_val, imported_val, parameter,
                                       method_define_var, method_use_field,
                                       'module')
        write_result_to_json(create_file_path(output + '\\measureResult', 'measure_result.json'), module_dic)
        write_result_to_csv(create_file_path(output + '\\measureResult', 'measure_result_class.csv'),
                            create_file_path(output + '\\measureResult', 'measure_result_method.csv'), module_dic)
        return True
    return False


def measure_package_metrics(dep_path, output):
    # execute2 = "java -jar {} {}".format(base_dir +
    #                                     '/utils/commitextractor/commit.jar', project_path)
    # os.system(execute2)

    module_data = list()
    dep_dic = read_file(dep_path)
    if dep_dic:
        package_info, method_class, call, called, dep, inherit, descendent, override, overrided, import_val, imported_val, parameter, method_define_var, method_use_field = get_rel_info(
            dep_dic, dict(), output)
        package_dic = get_module_metric(dep_dic['variables'], package_info, inherit, descendent, method_class, dep,
                                        call, called, override, overrided, import_val, imported_val, parameter,
                                        method_define_var,
                                        method_use_field, 'package', module_data)
        write_result_to_json(create_file_path(output + '\\measureResult', 'measure_result.json'), package_dic)
        write_result_to_csv(create_file_path(output + '\\measureResult', 'measure_result_class.csv'),
                            create_file_path(output + '\\measureResult', 'measure_result_method.csv'), package_dic)
    return module_data


def measure_multi_version(dep_path, output):
    project_list = list()
    version_list= os.listdir(dep_path)
    for ver in version_list:
        current_path = os.path.join(dep_path, ver)
        dep_file = os.listdir(current_path)[0]
        module_data = measure_package_metrics(os.path.join(current_path, dep_file), os.path.join(output, ver))
        tmp_pro = np.array(module_data).mean(axis=0).tolist()
        project_list.append(tmp_pro)

    project_list = np.around(project_list, 4)
    draw_line_chart(version_list, project_list, output)


def draw_line_chart(version_list, project_list, output):
    plt.title('change curve')
    # plt.plot(version_list, project_list, label=['SMQ', 'ODD', 'IDD', 'SPREAD', 'FOUCUS', 'ICF', 'ECF', 'REI'])
    plt.plot(version_list, project_list, label=['SCOH', 'SCOP', 'ODD', 'IDD'])
    plt.legend()
    plt.xlabel('version')
    plt.ylabel('quality score')
    plt.savefig(output + '/change.jpg')
    # plt.show()


def compare_diff(folder_path1, folder_path2, mapping, output):
    measure_json_dict1, dep_json_dict1 = read_folder(folder_path1, 'measure_result.json', 'dep.json')
    measure_json_dict2, dep_json_dict2 = read_folder(folder_path2, 'measure_result.json', 'dep.json')
    if mapping:
        pp_mapping = read_file(mapping)
        # convert result1's packages' old name to new name
        measure_json_dict1 = _convert_old_to_new(measure_json_dict1, pp_mapping)
    if not (measure_json_dict1 or measure_json_dict2 or dep_json_dict1 or dep_json_dict2):
        return False
    measure_diff = dict()
    dep_diff = dict()
    metric_change = list()
    modules_name = list()
    _get_measure_diff(measure_json_dict1, measure_json_dict2, measure_diff, modules_name, metric_change)
    _get_dep_diff(dep_json_dict1, dep_json_dict2, dep_diff)
    write_result_to_json(create_file_path(output + '\\diffResult', 'measure_diff.json'), measure_diff)
    write_result_to_json(create_file_path(output + '\\diffResult', 'dep_diff.json'), dep_diff)
    gen_xlsx(create_file_path(output + '\\diffResult', 'diff_result.xlsx'), metric_change, modules_name, measure_diff)
    return True


def _get_measure_diff(measure_json_dict1, measure_json_dict2, measure_diff, modules_name, metric_change):
    for module_name in measure_json_dict2:
        if module_name in measure_json_dict1:
            module_result1 = measure_json_dict1[module_name]
            module_result2 = measure_json_dict2[module_name]
            measure_diff[module_name] = {'scoh': float(format(module_result2['scoh'] - module_result1['scoh'], '.4f')),
                                         'scop': float(format(module_result2['scop'] - module_result1['scop'], '.4f')),
                                         'odd': float(format(module_result2['odd'] - module_result1['odd'], '.4f')),
                                         'idd': float(format(module_result2['idd'] - module_result1['idd'], '.4f')),
                                         'DSM': float(module_result2['DSM'] - module_result1['DSM'])}
            modules_name.append(module_name)
            metric_change.append([float(format(module_result2['scoh'] - module_result1['scoh'], '.4f')),
                                  float(format(module_result2['scop'] - module_result1['scop'], '.4f')),
                                  float(format(module_result2['odd'] - module_result1['odd'], '.4f')),
                                  float(format(module_result2['idd'] - module_result1['idd'], '.4f')),
                                  float(module_result2['DSM'] - module_result1['DSM'])])
            classes = dict()
            # 11->12 changed and added classes
            for class_name in module_result2['classes']:
                if class_name in module_result1['classes']:
                    class2 = module_result2['classes'][class_name]
                    class1 = module_result1['classes'][class_name]
                    _diff_classes(classes, class_name, class1, class2)
                    methods = dict()
                    for method_name in class2['methods']:
                        if method_name in class1['methods']:
                            method1_val = class1['methods'][method_name]
                            method2_val = class2['methods'][method_name]
                            _diff_methods(methods, method_name, method1_val, method2_val)
                        else:
                            methods[method_name] = class2['methods'][method_name]
                            methods[method_name]['status'] = 'add'
                    # 11->12 deleted methods
                    for method_name in class1['methods']:
                        if method_name not in class2['methods']:
                            methods[method_name] = class1['methods'][method_name]
                            methods[method_name]['status'] = 'delete'
                    classes[class_name]['methods'] = methods
                else:
                    classes[class_name] = module_result2['classes'][class_name]
                    classes[class_name]['status'] = 'add'
            # 11->12 deleted classes
            for class_name in module_result1['classes']:
                if class_name not in module_result2['classes']:
                    classes[class_name] = module_result1['classes'][class_name]
                    classes[class_name]['status'] = 'delete'

            measure_diff[module_name]['classes'] = classes


def _get_dep_diff(dep_json_dict1, dep_json_dict2, dep_diff):
    dep_diff['inherit'] = _get_diff(dep_json_dict1['inherit'], dep_json_dict2['inherit'])
    dep_diff['descendent'] = _get_diff(dep_json_dict1['descendent'], dep_json_dict2['descendent'])
    dep_diff['call'] = _get_diff(dep_json_dict1['call'], dep_json_dict2['call'])
    dep_diff['called'] = _get_diff(dep_json_dict1['called'], dep_json_dict2['called'])
    dep_diff['import'] = _get_diff(dep_json_dict1['import'], dep_json_dict2['import'])
    dep_diff['imported'] = _get_diff(dep_json_dict1['imported'], dep_json_dict2['imported'])


def _get_diff(dep_dic1, dep_dic2):
    result = dict()
    for dep_src_name in dep_dic2:
        if dep_src_name in dep_dic1:
            # 11->12 add
            for dep_dest_name2 in dep_dic2[dep_src_name]:
                if dep_dest_name2 not in dep_dic1[dep_src_name]:
                    if dep_src_name not in result:
                        result[dep_src_name] = list()
                    result[dep_src_name].append({'name': dep_dest_name2, 'status': 'add dep'})
            # 11->12 delete
            for dep_dest_name1 in dep_dic1[dep_src_name]:
                if dep_dest_name1 not in dep_dic2[dep_src_name]:
                    if dep_src_name not in result:
                        result[dep_src_name] = list()
                    result[dep_src_name].append({'name': dep_dest_name1, 'status': 'delete dep'})
        else:
            dep_dic2[dep_src_name].append('status:new class')
            result[dep_src_name] = dep_dic2[dep_src_name]
    return result


def _convert_old_to_new(old_name_ver_data, mapping):
    new_name_ver_data = dict()
    for module in old_name_ver_data:
        new_name = module
        for old_name in mapping:
            if old_name in module:
                new_name = module.replace(old_name, mapping[old_name])
                break
        new_name_ver_data[new_name] = {'scoh': old_name_ver_data[module]['scoh'],
                                       'scop': old_name_ver_data[module]['scop'],
                                       'idd': old_name_ver_data[module]['idd'],
                                       'odd': old_name_ver_data[module]['odd'],
                                       'DSM': old_name_ver_data[module]['DSM']}
        new_classes = dict()
        for class_name in old_name_ver_data[module]['classes']:
            new_class_name = class_name.replace(module, new_name)
            new_classes[new_class_name] = old_name_ver_data[module]['classes'][class_name]
        new_name_ver_data[new_name]['classes'] = new_classes
    return new_name_ver_data


def _diff_classes(classes, class_name, class1, class2):
    classes[class_name] = {'CIS': class2['CIS'] - class1['CIS'], 'NOM': class2['NOM'] - class1['NOM'],
                           'NAC': class2['NAC'] - class1['NAC'], 'NDC': class2['NDC'] - class1['NDC'],
                           'NOI': class2['NOI'] - class1['NOI'], 'NOID': class2['NOID'] - class1['NOID'],
                           'CTM': class2['CTM'] - class1['CTM'],
                           'IDCC': class2['IDCC'] - class1['IDCC'],
                           'IODD': class2['IODD'] - class1['IODD'],
                           'IIDD': class2['IIDD'] - class1['IIDD'],
                           'EDCC': class2['EDCC'] - class1['EDCC'],
                           'NOP': class2['NOP'] - class1['NOP'],
                           'c_chm': float(class2['c_chm']) - float(class1['c_chm']),
                           'c_chd': float(class2['c_chd']) - float(class1['c_chd']),
                           'c_FAN_IN': class2['c_FAN_IN'] - class1['c_FAN_IN'],
                           'c_FAN_OUT': class2['c_FAN_OUT'] - class1['c_FAN_OUT'],
                           'CBC': class2['CBC'] - class1['CBC'],
                           'c_variablesQty': class2['c_variablesQty'] - class1[
                               'c_variablesQty'],
                           'privateMethodsQty': class2['privateMethodsQty'] - class1[
                               'privateMethodsQty'],
                           'protectedMethodsQty': class2['protectedMethodsQty'] - class1[
                               'protectedMethodsQty'],
                           'staticMethodsQty': class2['staticMethodsQty'] - class1['staticMethodsQty'],
                           'defaultMethodsQty': class2['defaultMethodsQty'] - class1[
                               'defaultMethodsQty'],
                           'abstractMethodsQty': class2['abstractMethodsQty'] - class1[
                               'abstractMethodsQty'],
                           'finalMethodsQty': class2['finalMethodsQty'] - class1['finalMethodsQty'],
                           'synchronizedMethodsQty': class2['synchronizedMethodsQty'] - class1[
                               'synchronizedMethodsQty'],
                           'publicFieldsQty': class2['publicFieldsQty'] - class1['publicFieldsQty'],
                           'privateFieldsQty': class2['privateFieldsQty'] - class1['privateFieldsQty'],
                           'staticFieldsQty': class2['staticFieldsQty'] - class1['staticFieldsQty'],
                           'defaultFieldsQty': class2['defaultFieldsQty'] - class1['defaultFieldsQty'],
                           'finalFieldsQty': class2['finalFieldsQty'] - class1['finalFieldsQty'],
                           'synchronizedFieldsQty': class2['synchronizedFieldsQty'] - class1[
                               'synchronizedFieldsQty'],
                           'protectedFieldsQty': class2['protectedFieldsQty'] - class1[
                               'protectedFieldsQty'],
                           'RFC': class2['RFC'] - class1['RFC'], 'NOF': class2['NOF'] - class1['NOF'],
                           'NOVM': class2['NOVM'] - class1['NOVM'],
                           'NOSI': class2['NOSI'] - class1['NOSI'],
                           'TCC': class2['TCC'] - class1['TCC'],
                           'LCC': class2['LCC'] - class1['LCC'],
                           'LCOM': class2['LCOM'] - class1['LCOM'],
                           'LOCM*': class2['LOCM*'] - class1['LOCM*'],
                           'WMC': class2['WMC'] - class1['WMC'],
                           'c_modifiers': class2['c_modifiers'] - class1['c_modifiers']
                           }


def _diff_methods(methods, method_name, method1_val, method2_val):
    methods[method_name] = {'CBM': method2_val['CBM'] - method1_val['CBM'],
                            'm_FAN_IN': method2_val['m_FAN_IN'] - method1_val['m_FAN_IN'],
                            'm_FAN_OUT': method2_val['m_FAN_OUT'] - method1_val['m_FAN_OUT'],
                            'm_variablesQty': method2_val['m_variablesQty'] - method1_val[
                                'm_variablesQty'],
                            'IDMC': method2_val['IDMC'] - method1_val['IDMC'],
                            'EDMC': method2_val['EDMC'] - method1_val['EDMC'],
                            'IsOverride': _get_isOverride(method1_val['IsOverride'], method2_val['IsOverride']),
                            'OverridedQty': method2_val['OverridedQty'] - method1_val['OverridedQty'],
                            'methodsInvokedQty': method2_val['methodsInvokedQty'] - method1_val[
                                'methodsInvokedQty'],
                            'methodsInvokedLocalQty': method2_val['methodsInvokedLocalQty'] -
                                                      method1_val['methodsInvokedLocalQty'],
                            'methodsInvokedIndirectLocalQty': method2_val[
                                                                  'methodsInvokedIndirectLocalQty'] -
                                                              method1_val[
                                                                  'methodsInvokedIndirectLocalQty'],
                            'parametersQty': method2_val['parametersQty'] - method1_val[
                                'parametersQty']}


def _get_isOverride(method1_isOveeride_val, method2_isOveeride_val):
    # TRUE -> TRUE
    if method1_isOveeride_val and method2_isOveeride_val:
        return 0
    # FALSE -> FALSE
    if not method1_isOveeride_val and not method2_isOveeride_val:
        return 1
    # TRUE -> FALSE
    if method1_isOveeride_val and not method2_isOveeride_val:
        return 2
    # FALSE -> TRUE
    if not method1_isOveeride_val and method2_isOveeride_val:
        return 3
