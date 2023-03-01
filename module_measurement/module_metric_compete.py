import numpy as np
from object_oriented_measurement.class_metric_compete import class_and_method_metric_compete
from module_measurement.compete_strcut_dep import com_struct_metric
from util.metrics import *
from module_measurement.moduarity.sf_measure import get_spread_and_focus
from module_measurement.evolution.com_icf_ecf import get_icf_ecf_rei
from score_compete.index_measure import get_score


def get_module_metric(variables, package_info, inherit, descendent, method_class, struct_dep, call, called, override,
                      overrided, import_val, imported_val, parameter, method_define_var, method_use_field, type,
                      module_data, cmt_path):
    package_dic = dict()
    # measure history dep
    focus_dic, spread_dic, module_classes, commit = get_spread_and_focus(cmt_path, package_info, variables)
    icf_dic, ecf_dic, rei_dic = get_icf_ecf_rei(module_classes, commit)
    # measure structure dep
    module_list = list()
    c_count = 0
    m_num = 0
    for package in package_info:
        if type == 'module':
            package_name = package
        else:
            package_name = variables[package]['qualifiedName']
        module_value, idcc_list, edcc_list, fan_in, fan_out, iodd, iidd = com_struct_metric(package,
                                                                                            package_info,
                                                                                            struct_dep)
        module_value.extend(
            [spread_dic[package_name], focus_dic[package_name], icf_dic[package_name], ecf_dic[package_name],
             rei_dic[package_name]])
        # module_value.extend([0, 0, 0, 0, 0])
        class_dic, c_chm_list, c_chd_list, m_count = class_and_method_metric_compete(variables, package_info[package],
                                                                                     inherit, descendent, parameter,
                                                                                     method_define_var,
                                                                                     method_use_field, method_class,
                                                                                     call, called,
                                                                                     idcc_list, edcc_list, override,
                                                                                     overrided, import_val,
                                                                                     imported_val,
                                                                                     fan_in, fan_out, iodd, iidd)
        c_count += len(class_dic)
        m_num += m_count
        module_value.extend([np.mean(c_chm_list), np.mean(c_chd_list), len(package_info[package])])
        module_data.append(module_value[0:])
        module_metric = dict(zip(MODULE_METRICS, module_value))
        module_metric['classes'] = class_dic
        module_list.append([module_metric['scoh'], module_metric['scop'],
                            module_metric['odd'], module_metric['idd']])
        package_dic[package_name] = module_metric
    [normalized_result, score_result] = get_score(module_list,
                                                  [[0.25], [0.25], [0.25], [0.25]],
                                                  ['scoh', 'scop', 'odd', 'idd'])
    return package_dic, np.mean(score_result), c_count, m_num
