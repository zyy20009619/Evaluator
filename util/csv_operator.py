import csv


def write_to_csv(result_list, file_path):
    with open(file_path, "w", newline="", encoding='utf-8') as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerows(result_list)


def write_result_to_csv(class_file_path, method_file_path, content):
    class_f = open(class_file_path, 'w', encoding='utf-8', newline='')
    class_csv_writer = csv.writer(class_f)
    class_csv_writer.writerow(
        ["module_name", "scoh", "scop", "odd", "idd", "spread", "focus", "rei", "icf", "ecf", "DSM", "class_name",
         "c_chm", "c_chd", "CBC", "IDCC", "IODD",
         "IIDD", "EDCC", "c_FAN_IN", "c_FAN_OUT", "NAC", "NDC", "NOP", "NOI", "NOID", "RFC", "NOSI", "CTM", "NOM",
         "NOVM", "CIS",
         "privateMethodsQty", "protectedMethodsQty", "staticMethodsQty", 'defaultMethodsQty', 'abstractMethodsQty',
         'finalMethodsQty', 'synchronizedMethodsQty', "TCC", "LCC", "LCOM", "LCOM*", "WMC",
         "c_variablesQty", "NOF", "publicFieldsQty", "privateFieldsQty", "protectedFieldsQty", 'staticFieldsQty',
         'defaultFieldsQty', 'finalFieldsQty', 'synchronizedFieldsQty',
         "c_modifiers"])

    method_f = open(method_file_path, 'w', encoding='utf-8', newline='')
    method_csv_writer = csv.writer(method_f)
    method_csv_writer.writerow(
        ["module_name", "class_name", "method_name", "startLine", "CBM", "IDMC", "EDMC", "m_FAN_IN", "m_FAN_OUT",
         "IsOverride", "OverridedQty",
         "methodsInvokedQty", "methodsInvokedLocalQty", "methodsInvokedIndirectLocalQty", "m_variablesQty",
         "parametersQty", "m_modifiers"])
    for module_name in content:
        scoh = content[module_name]['scoh']
        scop = content[module_name]['scop']
        odd = content[module_name]['odd']
        idd = content[module_name]['idd']
        spread = content[module_name]['spread']
        focus = content[module_name]['focus']
        rei = content[module_name]['rei']
        icf = content[module_name]['icf']
        ecf = content[module_name]['ecf']
        DSM = content[module_name]['DSM']
        for class_name in content[module_name]['classes']:
            c_chm = content[module_name]['classes'][class_name]['c_chm']
            c_chd = content[module_name]['classes'][class_name]['c_chd']
            CIS = content[module_name]['classes'][class_name]['CIS']
            NOM = content[module_name]['classes'][class_name]['NOM']
            NAC = content[module_name]['classes'][class_name]['NAC']
            NDC = content[module_name]['classes'][class_name]['NDC']
            NOI = content[module_name]['classes'][class_name]['NOI']
            NOID = content[module_name]['classes'][class_name]['NOID']
            CTM = content[module_name]['classes'][class_name]['CTM']
            IDCC = content[module_name]['classes'][class_name]['IDCC']
            IODD = content[module_name]['classes'][class_name]['IODD']
            IIDD = content[module_name]['classes'][class_name]['IIDD']
            EDCC = content[module_name]['classes'][class_name]['EDCC']
            NOP = content[module_name]['classes'][class_name]['NOP']
            c_FAN_IN = content[module_name]['classes'][class_name]['c_FAN_IN']
            c_FAN_OUT = content[module_name]['classes'][class_name]['c_FAN_OUT']
            CBC = content[module_name]['classes'][class_name]['CBC']
            RFC = content[module_name]['classes'][class_name]['RFC']
            TCC = content[module_name]['classes'][class_name]['TCC']
            LCC = content[module_name]['classes'][class_name]['LCC']
            LCOM = content[module_name]['classes'][class_name]['LCOM']
            LCOM_norm = content[module_name]['classes'][class_name]['LOCM*']
            WMC = content[module_name]['classes'][class_name]['WMC']
            c_modifiers = content[module_name]['classes'][class_name]['c_modifiers']
            NOSI = content[module_name]['classes'][class_name]['NOSI']
            NOVM = content[module_name]['classes'][class_name]['NOVM']
            privateMethodsQty = content[module_name]['classes'][class_name]['privateMethodsQty']
            protectedMethodsQty = content[module_name]['classes'][class_name]['protectedMethodsQty']
            staticMethodsQty = content[module_name]['classes'][class_name]['staticMethodsQty']
            defaultMethodsQty = content[module_name]['classes'][class_name]['defaultMethodsQty']
            abstractMethodsQty = content[module_name]['classes'][class_name]['abstractMethodsQty']
            finalMethodsQty = content[module_name]['classes'][class_name]['finalMethodsQty']
            synchronizedMethodsQty = content[module_name]['classes'][class_name]['synchronizedMethodsQty']
            c_variablesQty = content[module_name]['classes'][class_name]['c_variablesQty']
            NOF = content[module_name]['classes'][class_name]['NOF']
            publicFieldsQty = content[module_name]['classes'][class_name]['publicFieldsQty']
            privateFieldsQty = content[module_name]['classes'][class_name]['privateFieldsQty']
            protectedFieldsQty = content[module_name]['classes'][class_name]['protectedFieldsQty']
            staticFieldsQty = content[module_name]['classes'][class_name]['staticFieldsQty']
            defaultFieldsQty = content[module_name]['classes'][class_name]['defaultFieldsQty']
            synchronizedFieldsQty = content[module_name]['classes'][class_name]['synchronizedFieldsQty']
            finalFieldsQty = content[module_name]['classes'][class_name]['finalFieldsQty']
            class_csv_writer.writerow(
                [module_name, scoh, scop, odd, idd, spread, focus, rei, icf, ecf, DSM, class_name, c_chm, c_chd, CBC,
                 IDCC, IODD, IIDD, EDCC,
                 c_FAN_IN, c_FAN_OUT, NAC, NDC, NOI, NOID, NOP, RFC, NOSI, CTM, NOM, NOVM, CIS, privateMethodsQty,
                 protectedMethodsQty, staticMethodsQty, defaultMethodsQty,
                 abstractMethodsQty, finalMethodsQty, synchronizedMethodsQty, TCC, LCC, LCOM, LCOM_norm, WMC,
                 c_variablesQty, NOF,
                 publicFieldsQty, privateFieldsQty, protectedFieldsQty, staticFieldsQty, defaultFieldsQty,
                 finalFieldsQty, synchronizedFieldsQty, c_modifiers])
            for method_name in content[module_name]['classes'][class_name]['methods']:
                startLine = content[module_name]['classes'][class_name]['methods'][method_name]['startLine']
                CBM = content[module_name]['classes'][class_name]['methods'][method_name]['CBM']
                m_FAN_IN = content[module_name]['classes'][class_name]['methods'][method_name]['m_FAN_IN']
                m_FAN_OUT = content[module_name]['classes'][class_name]['methods'][method_name]['m_FAN_OUT']
                m_variablesQty = content[module_name]['classes'][class_name]['methods'][method_name][
                    'm_variablesQty']
                IDMC = content[module_name]['classes'][class_name]['methods'][method_name]['IDMC']
                EDMC = content[module_name]['classes'][class_name]['methods'][method_name]['EDMC']
                IsOverride = content[module_name]['classes'][class_name]['methods'][method_name]['IsOverride']
                OverridedQty = content[module_name]['classes'][class_name]['methods'][method_name]['OverridedQty']
                methodsInvokedQty = content[module_name]['classes'][class_name]['methods'][method_name][
                    'methodsInvokedQty']
                methodsInvokedLocalQty = content[module_name]['classes'][class_name]['methods'][method_name][
                    'methodsInvokedLocalQty']
                methodsInvokedIndirectLocalQty = content[module_name]['classes'][class_name]['methods'][method_name][
                    'methodsInvokedIndirectLocalQty']
                parametersQty = content[module_name]['classes'][class_name]['methods'][method_name]['parametersQty']
                m_modifier = content[module_name]['classes'][class_name]['methods'][method_name]['m_modifier']
                method_csv_writer.writerow(
                    [module_name, class_name, method_name, startLine, CBM, IDMC, EDMC, m_FAN_IN, m_FAN_OUT, IsOverride,
                     OverridedQty, methodsInvokedQty,
                     methodsInvokedLocalQty, methodsInvokedIndirectLocalQty, m_variablesQty, parametersQty, m_modifier])

    class_f.close()
    method_f.close()

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
