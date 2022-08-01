import xlsxwriter
import numpy as np
from util.metrics import *
from operator import itemgetter


def gen_xlsx(file_path, metric_change, modules_name, result):
    workbook = xlsxwriter.Workbook(file_path)
    bold = workbook.add_format({'bold': 1})
    _gen_change_sheet(workbook, bold, metric_change, modules_name)
    _gen_hotmap_sheet(workbook, bold, metric_change, modules_name)
    _gen_diff_sheet(workbook, bold, result)
    workbook.close()


def _gen_change_sheet(workbook, bold, metric_change, modules_name):
    worksheet1 = workbook.add_worksheet('变化幅度')
    headings1 = ["module_name"]
    headings1.extend(MODULE_METRICS)
    worksheet1.write_row('A1', headings1, bold)
    for index1 in range(0, len(metric_change)):
        worksheet1.write_string('A' + str(index1 + 2), modules_name[index1])
        for index2 in range(0, len(metric_change[index1])):
            worksheet1.write_number(index1 + 1, index2 + 1, metric_change[index1][index2])


def _gen_hotmap_sheet(workbook, bold, metric_change, modules_name):
    worksheet1 = workbook.add_worksheet('演化趋势')
    headings1 = ["module_name"]
    headings1.extend(MODULE_METRICS)
    worksheet1.write_row('A1', headings1, bold)

    max = np.amax(metric_change, axis=0)
    min = np.amin(metric_change, axis=0)
    for index1 in range(0, len(metric_change)):
        worksheet1.write_string('A' + str(index1 + 2), modules_name[index1])
        for index2 in range(0, len(metric_change[index1])):
            if index2 == 0:
                norm_value = float(
                    format((metric_change[index1][index2] - min[index2]) / (max[index2] - min[index2]), '.4f'))
            else:
                norm_value = float(
                    format((max[index2] - metric_change[index1][index2]) / (max[index2] - min[index2]), '.4f'))
            worksheet1.write_number(index1 + 1, index2 + 1, norm_value)
    worksheet1.conditional_format(1, 1, len(metric_change) + 1, 10,
                                  {'type': '3_color_scale', 'min_color': '#F08080', 'max_color': '#006400'})


def _gen_diff_sheet(workbook, bold, result):
    worksheet2 = workbook.add_worksheet('class_diff_result')
    headings2 = ["module_name"]
    headings2.extend(MODULE_METRICS)
    headings2.append("class_name")
    headings2.extend(CLASS_METRICS)
    headings2.append("status")
    worksheet2.write_row('A1', headings2, bold)

    worksheet3 = workbook.add_worksheet('method_diff_result')
    headings3 = ["module_name", "class_name", "method_name"]
    headings3.extend(METHOD_METRICS)
    headings3.append("status")
    worksheet3.write_row('A1', headings3, bold)

    index1 = 1
    index2 = 1
    for module_name in result:
        module_value = list(itemgetter(*MODULE_METRICS)(result[module_name]))
        for class_name in result[module_name]['classes']:
            class_value = list(itemgetter(*CLASS_METRICS)(result[module_name]['classes'][class_name]))
            status = '' if 'status' not in result[module_name]['classes'][class_name] else \
                result[module_name]['classes'][class_name]['status']
            class_value_diff = list()
            class_value_diff.append(module_name)
            class_value_diff.extend(module_value)
            class_value_diff.append(class_name)
            class_value_diff.extend(class_value)
            class_value_diff.append(status)
            worksheet2.write_row(index1, 0, class_value_diff)
            for method_name in result[module_name]['classes'][class_name]['methods']:
                method_value = list(itemgetter(*METHOD_METRICS)(result[module_name]['classes'][class_name]['methods'][method_name]))
                status = '' if 'status' not in result[module_name]['classes'][class_name]['methods'][method_name] else \
                    result[module_name]['classes'][class_name]['methods'][method_name]['status']
                method_value_diff = list()
                method_value_diff.extend([module_name, class_name, method_name])
                method_value_diff.extend(method_value)
                method_value_diff.append(status)
                worksheet3.write_row(index2, 0, method_value_diff)
                index2 += 1
            index1 += 1
