import pandas as pd
import numpy as np
from module_measurement.compete_strcut_dep import com_call_coh, com_call_coup


def com_metrics(json_dic, base_out_path):
    cells = json_dic[0]['cells']
    variables = json_dic[0]['variables']
    get_rel(variables, cells)


def get_rel(variables, cells):
    # 暂时处理下,把id和type对应起来
    tmp_var_type = dict()
    tmp_var_name = dict()
    for v in variables:
        tmp_var_type[v['id']] = v['entityType']
        tmp_var_name[v['id']] = v['qualifiedName']

    file_define = dict()
    extend = dict()
    extended = dict()
    include = dict()
    included = dict()
    for c in cells:
        # Define(FileStruct)
        if c['type'] == 'Define' and tmp_var_type[c['src']] == 'File' and tmp_var_type[c['dest']] == 'Struct':
            if c['src'] not in file_define:
                file_define[c['src']] = list()
            file_define[c['src']].append(c['dest'])
        # Extend(StructStruct)
        if c['type'] == 'Extend' and tmp_var_type[c['src']] == 'Struct' and tmp_var_type[c['dest']] == 'Struct':
            _add_list_value(extend, c['src'], c['dest'])
            _add_list_value(extended, c['dest'], c['src'])
        # # Include(FileFile)
        # if c['type'] == 'Include' and variables[c['src']]['category'] == 'File' and variables[c['dest']][
        #     'category'] == 'File':
        #     _add_list_value(include, c['src'], c['dest'])
        #     _add_list_value(included, c['dest'], c['src'])
    # 汇总File之间的dep
    dep = get_dep(extend, extended, include, included)
    com_module(file_define, dep, variables)


def get_dep(extend, extended, include, included):
    struct_dep = include.extend(included)
    return struct_dep


#     file_dep = dict()
#     for f1 in file_define:
#         file_dep[f1] = dict()
#         for f2 in file_define:
#             # # 先对Include关系进行统计
#             # if f1 in extend and f2 in extended:
#             #     file_dep[f1][f2] = 1
#             # if f2 in extend and f1 in extended:
#             if f1 != f2:
#                 for s1 in file_define[f1]:
#                     for s2 in file_define[f2]:
#                         if s1 in include and s2 in included:
#                             if s1 not in file_dep:
#                                 file_dep[f1][f2] = 0
#                             file_dep[f1][f2] += 1
#                         if s2 in include and s1 in included:
#                             if s2 not in file_dep:
#                                 file_dep[f1][f2] = 0
#                             file_dep[f1][f2] += 1


def com_module(file_define, dep, variables):
    module_value = list()
    for file in file_define:
        scoh, idcc_list = com_call_coh(file_define[file], dep, dict(), dict(), dict(), dict())
        scop, odd, idd, edcc_list = com_call_coup(file, file_define, dep, dict(), dict())
        module_value.append([variables[file]['qualifiedName'], float(format(scoh, '.4f')), float(format(scop, '.4f')),
                             float(format(odd, '.4f')),
                             float(format(idd, '.4f'))])
    res = pd.DataFrame(data=module_value, columns=['file name', 'scoh', 'scop', 'odd', 'idd'])
    res['SMQ'] = np.mean(res['scoh']  - res['scop'])
    res['ODD'] = np.mean(res['odd'])
    res['IDD'] = np.mean(res['idd'])
    res.to_csv()


def _add_list_value(dic, id1, id2):
    if id1 not in dic:
        dic[id1] = list()
    dic[id1].append(id2)
