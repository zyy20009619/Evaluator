import xlsxwriter
import numpy as np


def gen_xlsx(file_path, metric_change, modules_name, result):
    workbook = xlsxwriter.Workbook(file_path)
    bold = workbook.add_format({'bold': 1})
    _gen_change_sheet(workbook, bold, metric_change, modules_name)
    _gen_hotmap_sheet(workbook, bold, metric_change, modules_name)
    _gen_diff_sheet(workbook, bold, result)
    workbook.close()


def _gen_hotmap_sheet(workbook, bold, metric_change, modules_name):
    worksheet1 = workbook.add_worksheet('演化趋势')
    headings1 = ["module_name", "scoh", "scop", "odd", "idd", "DSC"]
    worksheet1.write_row('A1', headings1, bold)

    max = np.amax(metric_change, axis=0)
    min = np.amin(metric_change, axis=0)
    for index1 in range(0, len(metric_change)):
        worksheet1.write_string('A' + str(index1 + 2), modules_name[index1])
        for index2 in range(0, len(metric_change[index1])):
            if len(metric_change) == 1:
                norm_value = 0
                worksheet1.write_number(index1 + 1, index2 + 1, norm_value)
                continue
            if index2 == 0:
                norm_value = float(
                    format((metric_change[index1][index2] - min[index2]) / (max[index2] - min[index2]), '.4f'))
            else:
                norm_value = float(
                    format((max[index2] - metric_change[index1][index2]) / (max[index2] - min[index2]), '.4f'))
            worksheet1.write_number(index1 + 1, index2 + 1, norm_value)
    worksheet1.conditional_format(1, 1, len(metric_change) + 1, 6,
                                  {'type': '3_color_scale', 'min_color': '#F08080', 'max_color': '#006400'})


def gen_diff_sheet(workbook, bold, result):
    worksheet2 = workbook.add_worksheet('diff_result')
    headings2 = ["module_name", "scoh", "scop", "odd", "idd", "DSM", "class_name", "CIS", "NOM", "NAC", "NDC", "CTM",
                 "IDCC", "EDCC", "DAM", "NOP", "status"]
    worksheet2.write_row('A1', headings2, bold)

    index = 1
    for module_name in result:
        scoh = result[module_name]['scoh']
        scop = result[module_name]['scop']
        odd = result[module_name]['odd']
        idd = result[module_name]['idd']
        DSM = result[module_name]['DSM']
        for class_name in result[module_name]['classes']:
            CIS = result[module_name]['classes'][class_name]['CIS']
            NOM = result[module_name]['classes'][class_name]['NOM']
            NAC = result[module_name]['classes'][class_name]['NAC']
            NDC = result[module_name]['classes'][class_name]['NDC']
            CTM = result[module_name]['classes'][class_name]['CTM']
            IDCC = result[module_name]['classes'][class_name]['IDCC']
            EDCC = result[module_name]['classes'][class_name]['EDCC']
            DAM = result[module_name]['classes'][class_name]['DAM']
            NOP = result[module_name]['classes'][class_name]['NOP']
            status = result[module_name]['classes'][class_name]['status']
            worksheet2.write_row(index, 0, [module_name, scoh, scop, odd, idd, DSM, class_name, CIS, NOM, NAC, NDC, CTM, IDCC,
                                                              EDCC, DAM, NOP, status])
            index += 1
