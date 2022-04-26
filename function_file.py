import json, csv
from module_measurement.module_metric_compete import get_module_metric
from analysis.indicate import gen_xlsx


def measure_module_metrics(dep_path, mapping_path):
    dep_dic = _read_file(dep_path)
    mapping_dic = _read_file(mapping_path)
    if dep_dic and mapping_dic:
        module_info, method_class, call, dep, inherit, descendent, override = _get_rel_info(dep_dic, mapping_dic)
        module_dic = get_module_metric(dep_dic['variables'], module_info, inherit, descendent, method_class, dep, call, override, 'module')
        _write_result_to_json('measure_result.json', module_dic)
        _write_result_to_csv('measure_result.csv', module_dic)
        return True
    return False


def measure_package_metrics(dep_path):
    dep_dic = _read_file(dep_path)
    if dep_dic:
        package_info, method_class, call, dep, inherit, descendent, override = _get_rel_info(dep_dic, dict())
        package_dic = get_module_metric(dep_dic['variables'], package_info, inherit, descendent, method_class, dep, call, override, 'package')
        _write_result_to_json('measure_result.json', package_dic)
        _write_result_to_csv('measure_result.csv', package_dic)
        return True
    return False


# def sort_dic_by_class(dic):
#     result_dic = dict()
#     name_to_value = dict()
#     for module_name in dic:
#         class_value = 0
#         class_value += abs(float(dic[module_name]['scoh']))
#         class_value += abs(float(dic[module_name]['scop']))
#         class_value += abs(float(dic[module_name]['odd']))
#         class_value += abs(float(dic[module_name]['idd']))
#         class_value += abs(int(dic[module_name]['DSM']))
#         name_to_value[module_name] = class_value
#     name_to_value = sorted(name_to_value.items(), key=lambda x: x[1], reverse=True)
#
#     for name in name_to_value:
#         result_dic[name[0]] = dic[name[0]]
#
#     return result_dic


def compare_diff(file_path1, file_path2, mapping):
    result1 = _read_file(file_path1)
    result2 = _read_file(file_path2)
    if mapping:
        pp_mapping = _read_file(mapping)
        # convert result1's packages' old name to new name
        result1 = _convert_old_to_new(result1, pp_mapping)
    if not (result1 or result2):
        return False
    result = dict()
    new_class = dict()
    metric_change = list()
    modules_name = list()
    for module_name in result2:
        if module_name in result1:
            module_result1 = result1[module_name]
            module_result2 = result2[module_name]
            result[module_name] = {'scoh': format(module_result2['scoh'] - module_result1['scoh'], '.4f'), 'scop':  format(module_result2['scop'] - module_result1['scop'], '.4f'), 'odd': format(module_result2['odd'] - module_result1['odd'], '.4f'), 'idd': format(module_result2['idd'] - module_result1['idd'], '.4f'), 'DSM': module_result2['DSM'] - module_result1['DSM']}
            modules_name.append(module_name)
            metric_change.append([float(format(module_result2['scoh'] - module_result1['scoh'], '.4f')), float(format(module_result2['scop'] - module_result1['scop'], '.4f')), float(format(module_result2['odd'] - module_result1['odd'], '.4f')), float(format(module_result2['idd'] - module_result1['idd'], '.4f')), float(module_result2['DSM'] - module_result1['DSM'])])
            classes = dict()
            # 11->12 changed and added classes
            for class_name in module_result2['classes']:
                if class_name in module_result1['classes']:
                    class2 = module_result2['classes'][class_name]
                    class1 = module_result1['classes'][class_name]
                    classes[class_name] = {'CIS': class2['CIS'] - class1['CIS'], 'NOM':  class2['NOM'] - class1['NOM'], 'NAC':  class2['NAC'] - class1['NAC'], 'NDC':  class2['NDC'] - class1['NDC'], 'CTM':  class2['CTM'] - class1['CTM'], 'IDCC':  class2['IDCC'] - class1['IDCC'], 'EDCC':  class2['EDCC'] - class1['EDCC'], 'DAM':  format(float(class2['DAM']) - float(class1['DAM']), '.4f'), 'NOP':  class2['NOP'] - class1['NOP']}
                    classes[class_name]['status'] = 'change'
                else:
                    classes[class_name] = module_result2['classes'][class_name]
                    classes[class_name]['status'] = 'add'
                    if module_name not in new_class:
                        new_class[module_name] = list()
                    new_class[module_name].append(class_name)
            # 11->12 deleted classes
            for class_name in module_result1['classes']:
                if class_name not in module_result2['classes']:
                    classes[class_name] = module_result1['classes'][class_name]
                    classes[class_name]['status'] = 'delete'

            result[module_name]['classes'] = classes
    _write_result_to_json('diff_result.json', result)
    gen_xlsx('diff_result.xlsx', metric_change, modules_name, result)
    return True


def _convert_old_to_new(old_name_ver_data, mapping):
    new_name_ver_data = dict()
    for module in old_name_ver_data:
        new_name = module
        for old_name in mapping:
            if old_name in module:
                new_name = module.replace(old_name, mapping[old_name])
                break
        new_name_ver_data[new_name] = {'scoh': old_name_ver_data[module]['scoh'], 'scop': old_name_ver_data[module]['scop'], 'idd': old_name_ver_data[module]['idd'], 'odd': old_name_ver_data[module]['odd'], 'DSM': old_name_ver_data[module]['DSM']}
        new_classes = dict()
        for class_name in old_name_ver_data[module]['classes']:
            new_class_name = class_name.replace(module, new_name)
            new_classes[new_class_name] = old_name_ver_data[module]['classes'][class_name]
        new_name_ver_data[new_name]['classes'] = new_classes
    return new_name_ver_data


def _read_file(file_path):
    try:
        with open(file_path, 'r') as f:
            json_dict = json.load(f)
    except (FileExistsError, FileNotFoundError, PermissionError):
        json_dict = dict()
    return json_dict


def _write_result_to_json(file_path, content):
    with open(file_path, 'w') as f:
        json.dump(content, f, indent=4)


def _write_result_to_csv(file_path, content):
    f = open(file_path, 'w', encoding ='utf-8', newline = '')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["module_name", "scoh", "scop", "odd", "idd", "DSM", "class_name", "CIS", "NOM", "NAC", "NDC", "CTM", "IDCC", "EDCC", "DAM", "NOP"])
    for module_name in content:
        scoh = content[module_name]['scoh']
        scop = content[module_name]['scop']
        odd = content[module_name]['odd']
        idd = content[module_name]['idd']
        DSM = content[module_name]['DSM']
        for class_name in content[module_name]['classes']:
            CIS = content[module_name]['classes'][class_name]['CIS']
            NOM = content[module_name]['classes'][class_name]['NOM']
            NAC = content[module_name]['classes'][class_name]['NAC']
            NDC = content[module_name]['classes'][class_name]['NDC']
            CTM = content[module_name]['classes'][class_name]['CTM']
            IDCC = content[module_name]['classes'][class_name]['IDCC']
            EDCC = content[module_name]['classes'][class_name]['EDCC']
            DAM = content[module_name]['classes'][class_name]['DAM']
            NOP = content[module_name]['classes'][class_name]['NOP']
            csv_writer.writerow([module_name, scoh, scop, odd, idd, DSM, class_name, CIS, NOM, NAC, NDC, CTM, IDCC, EDCC, DAM, NOP])
    f.close()


# def write_result_to_excel(file_path, content, type_name, CIS_list, NOM_list, NAC_list, NDC_list, CTM_list, DCC_list, DAM_list, NOP_list, new_class):
#     # 创建一个excel
#     workbook = xlsxwriter.Workbook(file_path)
#     # 自定义样式，加粗
#     bold = workbook.add_format({'bold': 1})
#     # 创建一个演化趋势sheet页
#     sheet_name1 = '演化趋势'
#     worksheet1 = workbook.add_worksheet(sheet_name1)
#     # 写入表头
#     headings1 = ["module_name", "scoh", "scop", "odd", "idd", "DSC"]
#     worksheet1.write_row('A1', headings1, bold)
#     # 写入数据(变化趋势有好有坏,好的用绿色标识,坏的用红色标识(程度用深浅表示))
#
#
#
#     diff_list = list()
#     index1 = 2
#     index2 = 2
#     for module_name in content:
#         scoh = content[module_name]['scoh']
#         scop = content[module_name]['scop']
#         odd = content[module_name]['odd']
#         idd = content[module_name]['idd']
#         DSC = content[module_name]['DSC']
#         worksheet1.write_row('A' + str(index1), [module_name, scoh, scop, odd, idd, DSC])
#         diff_list.append(scoh)
#         diff_list.append(scop)
#         diff_list.append(odd)
#         diff_list.append(idd)
#         # dsc_list.append(DSC)
#         index1 += 1
#         for class_name in content[module_name]['classes']:
#             CIS = content[module_name]['classes'][class_name]['CIS']
#             NOM = content[module_name]['classes'][class_name]['NOM']
#             NOP = content[module_name]['classes'][class_name]['NOP']
#             NAC = content[module_name]['classes'][class_name]['NAC']
#             NDC = content[module_name]['classes'][class_name]['NDC']
#             CTM = content[module_name]['classes'][class_name]['CTM']
#             DAM = content[module_name]['classes'][class_name]['DAM']
#             DCC = content[module_name]['classes'][class_name]['DCC']
#
#             worksheet2.write_string(index2, 1, CIS, get_cell_format(CIS, workbook, CIS_outliers, get_new_classes(new_class, module_name), class_name))
#             worksheet2.write_string(index2, 2, NOM, get_cell_format(NOM, workbook, NOM_outliers, get_new_classes(new_class, module_name), class_name))
#             worksheet2.write_string(index2, 3, NOP, get_cell_format(NOP, workbook, NOP_outliers, get_new_classes(new_class, module_name), class_name))
#             worksheet2.write_string(index2, 4, NAC, get_cell_format(NAC, workbook, NAC_outliers, get_new_classes(new_class, module_name), class_name))
#             worksheet2.write_string(index2, 5, NDC, get_cell_format(NDC, workbook, NDC_outliers, get_new_classes(new_class, module_name), class_name))
#             worksheet2.write_string(index2, 6, CTM, get_cell_format(CTM, workbook, CTM_outliers, get_new_classes(new_class, module_name), class_name))
#             # worksheet2.write_string(index2, 7, DAM, get_cell_format(DAM, workbook, DAM_outliers, get_new_classes(new_class, module_name), class_name))
#             worksheet2.write_string(index2, 8, DCC, get_cell_format(DCC, workbook, DCC_outliers, get_new_classes(new_class, module_name), class_name))
#             # worksheet2.write_row('A' + str(index2), [module_name, class_name, CIS, NOM, NOP, NAC, NDC, CTM, DAM, DCC])
#             index2 += 1
#     if type_name == 'diff':
#         scoh_data = {
#             'name': 'scoh',
#             'categories': [sheet_name1, 0, 0, index1 - 1, 0],
#             'values': [sheet_name1, 0, 1, index1 - 1, 1],
#         }
#         scop_data = {
#             'name': 'scop',
#             'categories': [sheet_name1, 1, 0, index1 - 1, 0],
#             'values': [sheet_name1, 1, 2, index1 - 1, 2]
#         }
#         odd_data = {
#             'name': 'odd',
#             'categories': [sheet_name1, 1, 0, index1 - 1, 0],
#             'values': [sheet_name1, 1, 3, index1 - 1, 3]
#         }
#         idd_data = {
#             'name': 'idd',
#             'categories': [sheet_name1, 1, 0, index1 - 1, 0],
#             'values': [sheet_name1, 1, 4, index1 - 1, 4]
#         }
#         dsc_data = {
#             'name': 'DSC',
#             'categories': [sheet_name1, 0, 0, index1 - 1, 0],
#             'values': [sheet_name1, 0, 5, index1 - 1, 5],
#         }
#         # write_chart_to_excel(workbook, worksheet1, '指标变化幅度(scoh/scop/odd/idd)', 'column', 'H2', [scoh_data, scop_data, odd_data, idd_data], 0, 0)
#         # write_chart_to_excel(workbook, worksheet1, 'DSC指标变化幅度', 'column', 'Q2', [dsc_data], 0, 0)
#         write_chart_to_excel(workbook, worksheet1, 'scoh', 'column', 'H2', [scoh_data], 0, 0)
#         write_chart_to_excel(workbook, worksheet1, 'scop', 'column', 'Q2', [scop_data], 0, 0)
#         write_chart_to_excel(workbook, worksheet1, 'odd', 'column', 'H18', [odd_data], 0, 0)
#         write_chart_to_excel(workbook, worksheet1, 'idd', 'column', 'Q18', [idd_data], 0, 0)
#         write_chart_to_excel(workbook, worksheet1, 'DSC', 'column', 'H34', [dsc_data], 0, 0)
#     workbook.close()
#
#
# def get_new_classes(new_class, module_name):
#     if module_name in new_class:
#         return new_class[module_name]
#     return list()
#
#
# def get_cell_format(value, workbook, outliers, module_classes, class_name):
#     if class_name in module_classes:
#         cell_format = workbook.add_format({'bold': True, 'font_color': 'gray'})
#     elif value > outliers:
#         cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
#     return cell_format
#
#
# def write_chart_to_excel(workbook, worksheet, title_name, type_name, insert_pos, data, min, max):
#     # 创建一个柱状图
#     chart = workbook.add_chart({'type': type_name})
#     # 配置系列数据
#     # chart.add_series(data[0])
#     for d in data:
#         chart.add_series(d)
#     # 把图表插入到worksheet并设置偏移
#     chart.set_title({'name': title_name})
#     if not (max == 0 and min == 0):
#         chart.set_y_axis({'min': min, 'max': max})
#     worksheet.insert_chart(insert_pos, chart)


def _get_rel_info(json_dic, mapping_dic):
    cells = json_dic['cells']
    variables = json_dic['variables']

    class_contain = dict()
    package_contain = dict()
    package_name_to_id = dict()
    file_contain = dict()
    inherit = dict()
    descendent = dict()
    override = dict()
    dep = dict()
    call = dict()
    method_class = dict()
    for c in cells:
        # Contain
        if 'Contain' in c['values']:
            if variables[c['src']]['category'] == 'Class':
                if c['src'] not in class_contain:
                    class_contain[c['src']] = list()
                class_contain[c['src']].append(c['dest'])
                if variables[c['dest']]['category'] == 'Method':
                    method_class[c['dest']] = c['src']
            if variables[c['src']]['category'] == 'Package' and variables[c['dest']]['category'] == 'File':
                if c['src'] not in package_contain:
                    package_contain[c['src']] = list()
                package_contain[c['src']].append(c['dest'])
                package_name_to_id[variables[c['src']]['qualifiedName']] = c['src']
            if variables[c['src']]['category'] == 'File' and variables[c['dest']]['category'] == 'Class':
                file_contain[c['src']] = c['dest']
        # Inherit
        if 'Inherit' in c['values']:
            if c['dest'] not in descendent:
                descendent[c['dest']] = list()
            if c['src'] not in inherit:
                inherit[c['src']] = list()
            if c['src'] not in dep:
                dep[c['src']] = dict()
            if c['dest'] not in dep[c['src']]:
                dep[c['src']][c['dest']] = 0
            dep[c['src']][c['dest']] += 1
            descendent[c['dest']].append(c['src'])
            inherit[c['src']].append(c['dest'])
        if 'Import' in c['values'] or 'Implement' in c['values']:
            if c['src'] not in dep:
                dep[c['src']] = dict()
            if c['dest'] not in dep[c['src']]:
                dep[c['src']][c['dest']] = 0
            dep[c['src']][c['dest']] += 1
        if 'Call' in c['values']:
            if c['src'] in method_class and c['dest'] in method_class and method_class[c['src']] != method_class[c['dest']]:
                if c['src'] not in call:
                    call[c['src']] = list()
                call[c['src']].append(c['dest'])
                if method_class[c['src']] not in dep:
                    dep[method_class[c['src']]] = dict()
                if method_class[c['dest']] not in dep[method_class[c['src']]]:
                    dep[method_class[c['src']]][method_class[c['dest']]] = 0
                dep[method_class[c['src']]][method_class[c['dest']]] += 1
        if 'Override' in c['values']:
            override[c['src']] = c['dest']

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
                    module_info[package][file_contain[file]] = class_contain[file_contain[file]]
            if len(module_info[package]) == 0:
                del module_info[package]

    return module_info, method_class, call, dep, inherit, descendent, override
