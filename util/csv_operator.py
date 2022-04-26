import csv


def write_to_csv(result_list, file_path):
    with open(file_path, "w", newline="", encoding='utf-8') as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerows(result_list)


def write_result_to_csv(class_file_path, method_file_path, content):
    class_f = open(class_file_path, 'w', encoding='utf-8', newline='')
    class_csv_writer = csv.writer(class_f)
    class_csv_writer.writerow(
        ["module_name", "scoh", "scop", "odd", "idd", "DSM", "class_name",
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
                [module_name, scoh, scop, odd, idd, DSM, class_name, c_chm, c_chd, CBC,
                 IDCC, IODD, IIDD, EDCC,
                 c_FAN_IN, c_FAN_OUT, NAC, NDC, NOI, NOID, NOP, RFC, NOSI, CTM, NOM, NOVM, CIS, privateMethodsQty,
                 protectedMethodsQty, staticMethodsQty, defaultMethodsQty, abstractMethodsQty, finalMethodsQty,
                 synchronizedMethodsQty, TCC, LCC, LCOM, LCOM_norm, WMC, c_variablesQty, NOF,
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