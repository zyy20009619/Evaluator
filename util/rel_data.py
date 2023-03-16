import os.path

from collections import defaultdict

from util.json_operator import write_result_to_json
from util.path_operator import create_file_path


def get_rel_info(json_dic, lang):
    # TODO:如果后期依赖模型统一，请修改此处
    if lang == 'c':
        variables = json_dic[0]['variables']
        cells = json_dic[0]['relations']
        var_id_to_var, file_contain, file_dep_matrix, struct_dep_matrix, function_dep = get_c_rel(variables, cells)
    else:
        variables = json_dic['variables']
        cells = json_dic['cells']
        get_java_rel(variables, cells)
    return var_id_to_var, file_contain, file_dep_matrix, struct_dep_matrix, function_dep


def get_three_model(first_contain, second_contain):
    for c1 in first_contain:
        for c2 in first_contain[c1]:
            if c2 in second_contain:
                first_contain[c1][c2] = second_contain[c2]


def get_c_rel(variables, cells):
    var_id_to_var = dict()
    struct_contain = dict()
    # struct->function关系构建：对所有变量进行扫描，如果变量的category是Typedef且其ParentId对应的实体category是Struct，那么认为该变量是struct下的函数
    for var in variables:
        var_id_to_var[var['id']] = var
    # TODO:Funtion和Function Pointer可以对应起来之后进行该层映射
    # for var in variables:
    #     # if 'type' in var and var['type'] in var_id_to_var:
    #     #     typevar = var_id_to_var[var['type']]
    #     if 'typedefType' in var and var['typedefType'] == 'Function Pointer' and var_id_to_var[var['parentID']]['category'] == 'Struct':
    #         if var['parentID'] not in struct_contain:
    #             struct_contain[var['parentID']] = list()
    #         struct_contain[var['parentID']].append(var['id'])

    file_contain = dict()
    # 构造依赖矩阵
    file_dep_matrix = dict()
    struct_dep_matrix = dict()
    para_dep_matrix = dict()
    typeuse_dep_matrix = dict()
    call_dep_matrix = dict()
    for cell in cells:
        # Define:用于构建file->struct
        con_rel_info(var_id_to_var, cell, 'Define', file_contain, 'File', 'Struct')
        con_rel_info(var_id_to_var, cell, 'Define', file_contain, 'File', 'Function')
        # Include:用于构建file include file关系
        con_rel_info(var_id_to_var, cell, 'Include', file_dep_matrix, 'File', 'File')
        # Embed
        con_rel_info(var_id_to_var, cell, 'Embed', struct_dep_matrix, 'Struct', 'Struct')
        # Parameter
        con_rel_info(var_id_to_var, cell, 'Parameter', para_dep_matrix, 'Function', 'Typedef')
        # typeUse
        con_rel_info(var_id_to_var, cell, 'typeUse', typeuse_dep_matrix, 'Function', 'Struct')
        # Call
        # con_rel_info(var_id_to_var, cell, 'Call', call_dep_matrix, 'Function', 'Typedef')
        con_rel_info(var_id_to_var, cell, 'Call', call_dep_matrix, 'Function', 'Function')
    # 构建三层模型结构->第一层:module(package<java>/file<c>)+第二层:class<java>+struct<c>+第三层:method<java>+typedef<c>
    # get_three_model(file_contain, struct_contain)
    function_dep = {'typeuse_dep': typeuse_dep_matrix, 'call_dep': call_dep_matrix, 'para_dep': para_dep_matrix}
    return var_id_to_var, file_contain, file_dep_matrix, struct_dep_matrix, function_dep


def con_rel_info(variables, cell, cell_type, dep_matrix, from_type, to_type):
    if cell['type'] == cell_type:
        if cell['src'] in variables and cell['dest'] in variables:
            if cell_type == 'Parameter':
                add_dep_to_dict(cell['src'], cell['dest'], dep_matrix)
                return
            if variables[cell['src']]['category'] == from_type and variables[cell['dest']]['category'] == to_type:
                if cell_type == 'Define':
                    if cell['src'] not in dep_matrix:
                        dep_matrix[cell['src']] = dict()
                    dep_matrix[cell['src']][cell['dest']] = list()
                    return
                add_dep_to_dict(cell['src'], cell['dest'], dep_matrix)
                # add_dep_to_dict(cell['dest'], cell['src'], dep_matrix)


def add_dep_to_dict(src_id, dest_id, dic):
    if src_id not in dic:
        dic[src_id] = dict()
    if dest_id not in dic[src_id]:
        dic[src_id][dest_id] = 0
    dic[src_id][dest_id] += 1


def get_java_rel(variables, cells):
    module_contain = dict()
    class_contain = dict()
    method_define_var = dict()
    method_use_field = dict()
    package_name_to_id = dict()
    file_contain = dict()
    set_var = dict()
    inherit = dict()
    descendent = dict()
    override = dict()
    parameter = dict()
    overrided = dict()
    dep = dict()
    call = dict()
    called = dict()
    import_val = dict()
    imported_val = dict()
    method_class = dict()
    for c in cells:
        # Define
        if 'Define' in c['values']:
            if variables[c['src']]['category'] == 'Class':
                if c['src'] not in class_contain:
                    class_contain[c['src']] = list()
                class_contain[c['src']].append(c['dest'])
                if variables[c['dest']]['category'] == 'Method':
                    method_class[c['dest']] = c['src']
            if variables[c['src']]['category'] == 'Method' and variables[c['dest']]['category'] == 'Variable':
                if c['src'] not in method_define_var:
                    method_define_var[c['src']] = set(list())
                method_define_var[c['src']].add(c['dest'])
        # Set
        if 'Set' in c['values']:
            if c['src'] not in set_var:
                set_var[c['src']] = list()
            set_var[c['src']].append(c['dest'])
        # Contain
        if 'Contain' in c['values']:
            if variables[c['src']]['category'] == 'Package' and variables[c['dest']]['category'] == 'File':
                if c['src'] not in module_contain:
                    module_contain[c['src']] = list()
                module_contain[c['src']].append(c['dest'])
                package_name_to_id[variables[c['src']]['qualifiedName']] = c['src']
            if variables[c['src']]['category'] == 'File' and variables[c['dest']]['category'] == 'Class':
                file_contain[c['src']] = c['dest']
        if variables[c['src']]['category'] == 'Method' and variables[c['dest']]['category'] == 'Variable':
            # UseVar
            if 'UseVar' in c['values']:
                if c['src'] not in method_use_field:
                    method_use_field[c['src']] = set(list())
                if variables[c['dest']]['global']:
                    method_use_field[c['src']].add(c['dest'])
            # Parameter
            if 'Parameter' in c['values']:
                if c['src'] not in parameter:
                    parameter[c['src']] = list()
                parameter[c['src']].append(c['dest'])
        # Inherit/Import/Implement/Cast/Reflect/Annotate
        if 'Inherit' in c['values'] or 'Import' in c['values'] or 'Implement' in c['values']:
            if 'Inherit' in c['values']:
                _add_list_value(inherit, c['src'], c['dest'])
                _add_list_value(descendent, c['dest'], c['src'])
            if 'Import' in c['values']:
                _add_list_value(import_val, c['src'], c['dest'])
                _add_list_value(imported_val, c['dest'], c['src'])
            _add_dep(dep, c['src'], c['dest'])
        if 'Call' in c['values']:
            _add_list_value(call, c['src'], c['dest'])
            _add_list_value(called, c['dest'], c['src'])
        # Call non-dynamic/Override (they have included in inherit, so don't need to be added in dep)
        if 'Call non-dynamic' in c['values'] or 'Override' in c['values']:
            override[c['src']] = c['dest']
            _add_list_value(overrided, c['dest'], c['src'])

    # # 将方法级依赖映射到类级别：call/use/parameter -> dep
    # convert_call_to_dep(call, method_class, dep)
    # # moduleinfo: class -> field/method
    #
    # # save call/called/inherit/descendent/import_val/imported_val into a dep file
    # _save_dep_to_json(inherit, descendent, call, called, import_val, imported_val, parameter,
    #                   variables, os.path.join(base_out_path, 'dep.json'))
    #
    # return module_info, method_class, call, called, dep, inherit, descendent, override, overrided, import_val, imported_val, parameter, method_define_var, method_use_field


def _save_dep_to_json(inherit, descendent, call_id_dic, called_id_dic, import_val, imported_val,
                      parameter, variables, dep_path):
    result = dict()
    result['inherit'] = _convert_dep_name_dic(inherit, variables)
    result['descendent'] = _convert_dep_name_dic(descendent, variables)
    result['import'] = _convert_dep_name_dic(import_val, variables)
    result['imported'] = _convert_dep_name_dic(imported_val, variables)
    result['call'] = _convert_call_method_name_dic(call_id_dic, parameter, variables)
    result['called'] = _convert_call_method_name_dic(called_id_dic, parameter, variables)
    write_result_to_json(dep_path, result)


def _convert_dep_name_dic(id_dic, variables):
    result = dict()
    for src_id in id_dic:
        if variables[src_id]['qualifiedName'] not in result:
            result[variables[src_id]['qualifiedName']] = list()
        for dest_id in id_dic[src_id]:
            result[variables[src_id]['qualifiedName']].append(variables[dest_id]['qualifiedName'])
    return result


def _convert_call_method_name_dic(id_dic, parameter, variables):
    name_dic = dict()
    for method_id1 in id_dic:
        method_name1 = _get_method_name(method_id1, parameter, variables)
        if method_name1 not in name_dic:
            name_dic[method_name1] = list()
        for method_id2 in id_dic[method_id1]:
            name_dic[method_name1].append(_get_method_name(method_id2, parameter, variables))
    return name_dic


def _get_method_name(method_id, parameter, variables):
    if method_id not in parameter:
        return variables[method_id]['qualifiedName'] + '/0'
    return variables[method_id]['qualifiedName'] + '/' + str(len(parameter[method_id]))


def _add_dep(dic, src_id, dest_id):
    if src_id not in dic:
        dic[src_id] = dict()
    if dest_id not in dic[src_id]:
        dic[src_id][dest_id] = 0
    dic[src_id][dest_id] += 1


def _add_list_value(dic, id1, id2):
    if id1 not in dic:
        dic[id1] = list()
    dic[id1].append(id2)


def convert_call_to_dep(call, method_class, dep):
    for src_method_id in call:
        for dest_method_id in call[src_method_id]:
            if src_method_id in method_class and dest_method_id in method_class:
                if method_class[src_method_id] not in dep:
                    dep[method_class[src_method_id]] = dict()
                if method_class[dest_method_id] not in dep[method_class[src_method_id]]:
                    dep[method_class[src_method_id]][method_class[dest_method_id]] = 0
                dep[method_class[src_method_id]][method_class[dest_method_id]] += 1


def get_module_info(mapping_dic, package_contain, package_name_to_id, file_contain, class_contain, method_use_field,
                    set_var, variables):
    module_info = dict()
    if mapping_dic:
        for module in mapping_dic:
            packages = mapping_dic[module]
            module_info[module] = dict()
            for package in packages:
                for file in package_contain[package_name_to_id[package]]:
                    if file in file_contain and file_contain[file] in class_contain:
                        module_info[module][file_contain[file]] = class_contain[file_contain[file]]
                if len(module_info[module]) == 0:
                    del module_info[module]
    else:
        for package in package_contain:
            module_info[package] = dict()
            for file in package_contain[package]:
                if file in file_contain and file_contain[file] in class_contain:
                    contain_list = list()
                    for method_or_field_id in class_contain[file_contain[file]]:
                        contain_list.append(method_or_field_id)
                        if variables[method_or_field_id][
                            'category'] == 'Method' and method_or_field_id in method_use_field:
                            contain_list.extend(method_use_field[method_or_field_id])
                    if file_contain[file] in set_var:
                        contain_list.extend(set_var[file_contain[file]])
                    module_info[package][file_contain[file]] = list(set(contain_list))
            if len(module_info[package]) == 0:
                del module_info[package]
    return module_info
