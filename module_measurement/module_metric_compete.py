from object_oriented_measurement.oo_metric_compete import count_method_and_var
from module_measurement.compete_strcut_dep import com_struct_metric


def get_module_metric(variables, package_info, inherit, descendent, method_class, struct_dep, call, override, type):
    package_dic = dict()
    for package in package_info:
        if type == 'module':
            package_name = package
        else:
            package_name = variables[package]['qualifiedName']
        package_dic[package_name] = dict()
        scoh, scop, odd, idd, idcc_list, edcc_list = com_struct_metric(variables, package, package_info, struct_dep, method_class, call)
        package_dic[package_name]['scoh'] = float(format(scoh, '.4f'))
        package_dic[package_name]['scop'] = float(format(scop, '.4f'))
        package_dic[package_name]['odd'] = float(format(odd, '.4f'))
        package_dic[package_name]['idd'] = float(format(idd, '.4f'))
        package_dic[package_name]['DSM'] = len(package_info[package])
        class_dic = count_method_and_var(variables, package_info[package], inherit, descendent, method_class, call, idcc_list, edcc_list, override)
        package_dic[package_name]['classes'] = class_dic

    return package_dic