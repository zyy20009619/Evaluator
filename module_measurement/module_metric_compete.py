import threading

from object_oriented_measurement.class_metric_compete import class_and_method_metric_compete
from module_measurement.compete_strcut_dep import com_struct_metric
from module_measurement.moduarity.sf_measure import get_spread_and_focus
from module_measurement.evolution.com_icf_ecf import get_icf_ecf_rei


def get_module_metric(variables, package_info, inherit, descendent, method_class, struct_dep, call, called, override,
                      overrided, import_val, imported_val, parameter, method_define_var, method_use_field, cmt_path,
                      type):
    package_dic = dict()
    # measure history dep
    focus_dic, spread_dic, module_classes, commit = get_spread_and_focus(cmt_path, package_info, variables)
    icf_dic, ecf_dic, rei_dic = get_icf_ecf_rei(module_classes, commit)

    # packages_id = list(package_info.keys())
    # for i in range(0, int(len(package_info) / 50) + 1):
    #     if i * 50 + 50 > len(packages_id):
    #         part_packages_id = packages_id[i * 50, len(packages_id)]
    #     else:
    #         part_packages_id = packages_id[i * 50: i * 50 + 50]
    # for
    _com_metrics(variables, list(package_info.keys()), package_info, inherit, descendent, method_class,
                 struct_dep, call, called,
                 override, overrided, import_val, imported_val, parameter, method_define_var,
                 method_use_field,
                 type, package_dic, focus_dic, spread_dic, icf_dic, ecf_dic, rei_dic)
    print('end to compete metrics!')
    return package_dic


def _com_metrics(variables, packages_id, package_info, inherit, descendent, method_class, struct_dep, call, called,
                 override, overrided, import_val, imported_val, parameter, method_define_var, method_use_field,
                 type, package_dic, focus_dic, spread_dic, icf_dic, ecf_dic, rei_dic):
    # measure structure dep
    for package in packages_id:
        print('current package:', package)
        if type == 'module':
            package_name = package
        else:
            package_name = variables[package]['qualifiedName']
        package_dic[package_name] = dict()
        scoh, scop, odd, idd, idcc_list, edcc_list, fan_in, fan_out, iodd, iidd = com_struct_metric(package,
                                                                                                    package_info,
                                                                                                    struct_dep)
        package_dic[package_name]['scoh'] = float(format(scoh, '.4f'))
        package_dic[package_name]['scop'] = float(format(scop, '.4f'))
        package_dic[package_name]['odd'] = float(format(odd, '.4f'))
        package_dic[package_name]['idd'] = float(format(idd, '.4f'))
        package_dic[package_name]['spread'] = spread_dic[package_name]
        package_dic[package_name]['focus'] = focus_dic[package_name]
        package_dic[package_name]['icf'] = icf_dic[package_name]
        package_dic[package_name]['ecf'] = ecf_dic[package_name]
        package_dic[package_name]['rei'] = rei_dic[package_name]
        package_dic[package_name]['DSM'] = len(package_info[package])
        class_dic = class_and_method_metric_compete(variables, package_info[package], inherit, descendent, parameter,
                                                    method_define_var, method_use_field, method_class, call, called,
                                                    idcc_list, edcc_list, override, overrided, import_val, imported_val,
                                                    fan_in, fan_out, iodd, iidd)
        package_dic[package_name]['classes'] = class_dic

    return package_dic
