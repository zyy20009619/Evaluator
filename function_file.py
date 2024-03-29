import os
import sys
import shutil
import matplotlib.pyplot as plt
import numpy as np
from module_measurement.module_metric_compete import get_module_metric
from analysis.indicate import gen_xlsx
from util.rel_data import get_rel_info
from util.csv_operator import write_result_to_csv
from util.json_operator import read_file, write_result_to_json, read_folder
from util.path_operator import create_file_path
from util.metrics import *
from operator import itemgetter
from module_measurement.com_metrics import com_metrics

GIT_COMMAND = 'git log  --pretty=format:"commit %H(%ad)%nauthor:%an%ndescription:%s"  --date=format:"%Y-%m-%d %H:%M:%S" --numstat  --name-status  --reverse  >./master.txt'


def measure_package_metrics(project_path, dep_path, output, ver, lang, grau, apollo_list):
    base_out_path = os.path.join(output, ver)
    os.makedirs(base_out_path, exist_ok=True)
    project_name = os.path.basename(project_path)
    # if ver != '':
    # loc_count = os.popen('cloc .').read()
    # tmp_loc = loc_count.split('\n')
    # tmp_loc1 = tmp_loc[len(tmp_loc) - 3].split(' ')
    # loc = tmp_loc1[len(tmp_loc1) - 1]

    # print(sys.path[0])
    # print(sys.argv[0])
    # print(os.path.realpath(sys.executable))
    # print(os.path.dirname(os.path.realpath(sys.argv[0])))
    # execute = "java -jar {} {}".format(os.path.dirname(os.path.realpath(sys.executable)) + '/commit.jar', project_path)
    if lang == 'java':
        os.chdir(project_path)
        os.system("git checkout -f " + ver)
        os.system(GIT_COMMAND)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        if dep_path == '':
            os.system('java -Xmx20G -jar ./util/tools/enre_java.jar java ' + project_path + ' ' + project_name)
            if not os.path.exists(os.path.join(base_out_path, project_name + '-out.json')):
                shutil.move(project_name + '-enre-out/' + project_name + '-out.json', base_out_path)
                shutil.rmtree(project_name + '-enre-out')
        else:
            if not os.path.exists(os.path.join(dep_path, ver)):
                shutil.move(os.rename(os.listdir(os.path.join(dep_path, ver))[0], project_name + '-out.json'),
                            base_out_path)
        execute = "java -jar {} {}".format('./util/tools/commit.jar', project_path)
        os.system(execute)
        if not os.path.exists(os.path.join(base_out_path, 'cmt.csv')):
            shutil.move(os.path.join(project_path, 'cmt.csv'), base_out_path)
    module_data = list()
    dep_dic = read_file(os.path.join(base_out_path, project_name + '-out.json'))
    if dep_dic:
        if lang == 'java':
            package_info, method_class, call, called, dep, inherit, descendent, override, overrided, import_val, imported_val, parameter, method_define_var, method_use_field = get_rel_info(
                dep_dic, lang, grau, base_out_path)
            package_dic, score, c_count, m_count = get_module_metric(dep_dic['variables'], package_info, inherit,
                                                                     descendent, method_class, dep,
                                                                     call, called, override, overrided, import_val,
                                                                     imported_val, parameter,
                                                                     method_define_var,
                                                                     method_use_field, module_data,
                                                                     os.path.join(base_out_path, 'cmt.csv'), grau)
            result = list()
            for item in module_data:
                temp = [item[0] - item[1]]
                temp.extend(item[2: 11: 1])
                result.append(temp)
            tmp_pro = np.around(np.array(result).mean(axis=0).tolist(), 4)
            project_dic = dict()
            tmp_pro = np.insert(tmp_pro, 0, score)
            project_metric = dict(zip(PROJECT_METRICS, tmp_pro))
            project_metric['modules'] = package_dic
            project_dic[ver] = project_metric
            apollo_list.append(project_metric['SMQ'])
            write_result_to_json(os.path.join(base_out_path, 'measure_result.json'), project_dic)
            write_result_to_csv(os.path.join(base_out_path, 'measure_result_class.csv'),
                                os.path.join(base_out_path, 'measure_result_method.csv'), ver, project_dic)
            return score
        else:
            # 在获取依赖时分别适配C语言和Java语言
            var_id_to_var, file_contain, file_dep_matrix, struct_dep_matrix, function_dep = get_rel_info(dep_dic, lang, base_out_path)
            # 计算指标
            com_metrics(ver, var_id_to_var, file_contain, file_dep_matrix, struct_dep_matrix, function_dep, base_out_path)


def measure_multi_version(project_path, dep_path, output, opt, vers, obj, lang):
    project_list = list()
    project_path_list = project_path.split('?')
    dep_path_list = dep_path.split('?')
    version_list = vers.split('?')
    index = 0
    for ver in version_list:
        pro_path = project_path_list[0]
        dep_path = dep_path_list[0]
        if obj == 'extension':
            pro_path = project_path[index]
            dep_path = dep_path[index]
        mapping_dic = dict()
        tmp_pro = measure_package_metrics(pro_path, dep_path, output, ver, mapping_dic, lang)
        project_list.append(tmp_pro)
        index += 1

    project_list = np.around(project_list, 4)
    draw_line_chart(version_list, project_list, output)


def draw_line_chart(version_list, project_list, output):
    plt.title('change curve')
    plt.plot(version_list, project_list, label=PROJECT_METRICS)
    plt.legend()
    plt.xlabel('version')
    plt.ylabel('quality score')
    plt.savefig(output + '/change.jpg')


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
    return output + '\\diffResult'


def _get_measure_diff(measure_json_dict1, measure_json_dict2, measure_diff, modules_name, metric_change):
    module2_info = measure_json_dict2[list(measure_json_dict2.keys())[0]]['modules']
    module1_info = measure_json_dict1[list(measure_json_dict1.keys())[0]]['modules']
    for module_name in module2_info:
        if module_name in module1_info:
            module_result1 = module1_info[module_name]
            module_result2 = module2_info[module_name]
            module_value1 = list(itemgetter(*MODULE_METRICS)(module_result1))
            module_value2 = list(itemgetter(*MODULE_METRICS)(module_result2))
            module_diff_value = _diff_value(module_value1, module_value2)
            module_diff_dict = dict(zip(MODULE_METRICS, module_diff_value))
            measure_diff[module_name] = module_diff_dict
            modules_name.append(module_name)
            metric_change.append(module_diff_value)
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


def _diff_value(list1, list2):
    res = list()
    for i in range(len(list1)):
        res.append(float(list2[i]) - float(list1[i]))
    return res


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
    class_value1 = list(itemgetter(*CLASS_METRICS)(class1))
    class_value2 = list(itemgetter(*CLASS_METRICS)(class2))
    class_diff_value = _diff_value(class_value1, class_value2)
    class_diff_dict = dict(zip(CLASS_METRICS, class_diff_value))
    classes[class_name] = class_diff_dict


def _diff_methods(methods, method_name, method1_val, method2_val):
    method_value1 = list(itemgetter(*METHOD_METRICS)(method1_val))
    method_value2 = list(itemgetter(*METHOD_METRICS)(method2_val))
    method_diff_value = _diff_value(method_value1, method_value2)
    method_diff_dict = dict(zip(METHOD_METRICS, method_diff_value))
    methods[method_name] = method_diff_dict


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
