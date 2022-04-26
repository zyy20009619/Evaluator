from object_oriented_measurement.class_metric_compete import class_and_method_metric_compete
from module_measurement.compete_strcut_dep import com_struct_metric


def get_module_metric(variables, package_info, inherit, descendent, method_class, struct_dep, call, override, type):
    package_dic = dict()
    for package in package_info:
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
        package_dic[package_name]['DSM'] = len(package_info[package])
        class_dic = class_and_method_metric_compete(variables, package_info[package], inherit, descendent, parameter,
                                                    method_define_var, method_use_field, method_class, call, called,
                                                    idcc_list, edcc_list, override, overrided, import_val, imported_val,
                                                    fan_in, fan_out, iodd, iidd)
        package_dic[package_name]['classes'] = class_dic

    return package_dic
