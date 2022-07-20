import pandas as pd
from object_oriented_measurement.class_metric_compete import class_and_method_metric_compete
from module_measurement.compete_strcut_dep import com_struct_metric
from util.common import *
from module_measurement.moduarity.sf_measure import get_spread_and_focus
from module_measurement.evolution.com_icf_ecf import get_icf_ecf_rei


def get_module_metric(variables, package_info, inherit, descendent, method_class, struct_dep, call, called, override,
                      overrided, import_val, imported_val, parameter, method_define_var, method_use_field, type,
                      module_data, cmt_path):
    package_dic = dict()
    # measure history dep
    focus_dic, spread_dic, module_classes, commit = get_spread_and_focus(cmt_path, package_info, variables)
    icf_dic, ecf_dic, rei_dic = get_icf_ecf_rei(module_classes, commit)
    # measure structure dep
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
             rei_dic[package_name], len(package_info[package])])
        module_metric = dict(zip(MODULE_METRICS, module_value))
        class_dic = class_and_method_metric_compete(variables, package_info[package], inherit, descendent, parameter,
                                                    method_define_var, method_use_field, method_class, call, called,
                                                    idcc_list, edcc_list, override, overrided, import_val, imported_val,
                                                    fan_in, fan_out, iodd, iidd)
        module_metric['classes'] = class_dic
        package_dic[package_name] = module_metric
        module_data.append(module_value[0:-1])

    return package_dic
