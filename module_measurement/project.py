import csv
import pandas as pd
import numpy as np
import csv
from util.metrics import *
from operator import itemgetter
from score_compete.index_measure import get_score
from module_measurement.moduarity.sf_measure import get_spread_and_focus
from module_measurement.evolution.com_icf_ecf import get_icf_ecf_rei


class Method:
    def __init__(self, method_id, vars_info, cur_children_info, dep_info):
        self.__method = method_id
        self.__vars_info = vars_info
        self.__dep = dep_info
        self.__cur_children_info = cur_children_info
        self.startLine = 0
        self.CBM = 0
        self.m_FAN_IN = 0  # 被调用方法数(call)
        self.m_FAN_OUT = 0  # 调用方法数(call+typeuse)
        self.IDMC = 0  # 调用file内方法数量以及被本file内方法调用的数量
        self.EDMC = 0  # 调用file外方法数量以及被file外方法调用的数量
        self.methodsInvokedQty = 0  # 方法调用的所有方法数
        self.methodsInvokedLocalQty = 0  # 方法调用本file内的方法数
        self.methodsInvokedIndirectLocalQty = 0  # 间接调用本地方法的数量
        self.m_variablesQty = 0  # 暂无
        self.parametersQty = 0
        self.m_modifier = 0  # 数据里暂无
        # self.storage_class = ''
        self.__set_others()

    def __set_others(self):
        self.startLine = self.__vars_info[self.__method]['startLine']
        self.parametersQty = len(self.__dep['para_dep'][self.__method]) if self.__method in self.__dep[
            'para_dep'] else 0
        self.methodsInvokedQty = len(self.__dep['call_dep'][self.__method]) if self.__method in self.__dep[
            'call_dep'] else 0
        self.__set_local_qty()
        self.__com_rel()
        current_children_info = self.__cur_children_info
        current_method_id = self.__method
        self.m_variablesQty = len(self.__cur_children_info[self.__method]) if isinstance(
            current_children_info[current_method_id], dict) else 0
        self.CBM = self.m_FAN_IN + self.m_FAN_OUT

    def __set_local_qty(self):
        if self.__method in self.__dep['call_dep']:
            method_invocations_indirect_local = list()
            for called_id in self.__dep['call_dep'][self.__method]:
                if called_id in self.__cur_children_info:
                    self.methodsInvokedLocalQty += 1
                    # 处理间接调用本地方法的结果
                    method_invocations_indirect_local.extend(self.__get_called_values(
                        self.__invocation(called_id, dict(), self.__dep['call_dep'],
                                          self.__cur_children_info).values()))
            self.methodsInvokedIndirectLocalQty = len(set(method_invocations_indirect_local))

    def __invocation(self, method_id, explored, invoke_methods, local_contain):
        if method_id not in invoke_methods:
            return explored

        next_invocations = list()
        for called_id in invoke_methods[method_id]:
            if called_id not in explored and method_id != called_id and called_id in local_contain:
                next_invocations.append(called_id)
        if len(next_invocations) > 0:
            explored[method_id] = next_invocations
            for next_invocation in next_invocations:
                self.__invocation(next_invocation, explored, invoke_methods, local_contain)
        return explored

    def __get_called_values(self, arrays):
        res = list()
        for item1 in arrays:
            res.extend(item1)
        return res

    def __com_rel(self):
        self.m_FAN_OUT = self.methodsInvokedQty
        self.IDMC = self.methodsInvokedLocalQty
        self.EDMC = self.methodsInvokedQty - self.methodsInvokedLocalQty
        for call_id in self.__dep['call_dep']:
            if call_id != self.__method:
                if self.__method in self.__dep['call_dep'][call_id]:
                    self.m_FAN_IN += 1
                    if call_id in self.__cur_children_info:
                        self.IDMC += 1
                    else:
                        self.EDMC += 1
        # IDMC和EDMC也需考虑typeuse
        if self.__method in self.__dep['typeuse_dep']:
            self.m_FAN_OUT += len(self.__dep['typeuse_dep'][self.__method])
            for struct_id in self.__dep['typeuse_dep'][self.__method]:
                if struct_id in self.__cur_children_info:
                    self.IDMC += 1
                else:
                    self.EDMC += 1


class Class:
    def __init__(self, cur_class, vars_info, cur_children_info, dep_info):
        self.__class_id = cur_class
        self.__vars_info = vars_info
        self.__dep = dep_info
        self.__cur_children_info = cur_children_info
        self.c_chm = 0  # 暂无
        self.c_chd = 0  # 暂无
        self.CBC = 0  # 耦合的struct数量
        self.c_FAN_IN = 0
        self.c_FAN_OUT = 0
        self.IDCC = 0
        self.IODD = 0
        self.IIDD = 0
        self.EDCC = 0
        self.NOP = 0  # C语言暂无
        self.NAC = 0
        self.NDC = 0
        self.NOI = 0  # C语言暂无
        self.NOID = 0  # C语言暂无
        self.RFC = 0  # 暂无，加到file内
        self.NOSI = 0  # 暂无，加到file内
        self.CTM = 0  # 暂无，加到file内
        self.c_variablesQty = 0  # 暂无
        self.NOM = 0  # 统计Function Pointer数量
        self.WMC = 0  # 统计Function Pointer数量
        self.privateMethodsQty = 0  # 暂无
        self.NOVM = 0  # 暂无
        self.CIS = 0  # 暂无
        self.staticMethodsQty = 0  # 暂无
        self.defaultMethodsQty = 0  # 暂无
        self.abstractMethodsQty = 0  # 暂无
        self.finalMethodsQty = 0  # 暂无
        self.protectedMethodsQty = 0  # 暂无
        self.synchronizedMethodsQty = 0  # 暂无
        self.NOF = 0  # 暂无
        self.publicFieldsQty = 0  # 暂无
        self.privateFieldsQty = 0  # 暂无
        self.protectedFieldsQty = 0  # 暂无
        self.staticFieldsQty = 0  # 暂无
        self.defaultFieldsQty = 0  # 暂无
        self.finalFieldsQty = 0  # 暂无
        self.synchronizedFieldsQty = 0  # 暂无
        self.TCC = 0  # 暂无
        self.LCC = 0  # 暂无
        self.LCOM = 0  # 暂无
        self.LOCM1 = 0  # 暂无
        self.c_modifiers = 0  # 数据里暂无
        # self.methods = dict()
        self.__set_others()

    def __set_others(self):
        self.c_FAN_OUT = len(
            self.__dep[self.__class_id]) if self.__class_id in self.__dep else 0  # 暂时相等，后期struct出现其他依赖关系应考虑其他应该关系
        for stru in self.__dep:
            if stru == self.__class_id:
                for strued in self.__dep[self.__class_id]:
                    if strued in self.__cur_children_info:
                        self.IDCC += 1
                        self.IODD += 1
                    else:
                        self.EDCC += 1
            else:
                if self.__class_id in self.__dep[stru]:
                    self.c_FAN_IN += 1
                    if stru in self.__cur_children_info:
                        self.IDCC += 1
                        self.IIDD += 1
                    else:
                        self.EDCC += 1
        self.CBC = self.c_FAN_IN + self.c_FAN_OUT
        self.NAC = self.c_FAN_OUT
        self.NDC = self.c_FAN_IN
        current_children_info = self.__cur_children_info
        current_class_id = self.__class_id
        self.NOM = len(self.__cur_children_info[self.__class_id]) if isinstance(
            current_children_info[current_class_id], list) else 0
        self.WMC = self.NOM


class Module:
    def __init__(self, cur_module, vars_info, all_contain, dep_info):
        self.__cur_module = cur_module
        self.__all_contain = all_contain
        self.__children = all_contain[cur_module]
        self.__vars_info = vars_info
        self.__dep = dep_info
        self.scoh = 0
        self.scop = 0
        self.odd = 0
        self.idd = 0
        self.spread = 0  # 暂无
        self.focus = 0  # 暂无
        self.icf = 0  # 暂无
        self.ecf = 0  # 暂无
        self.rei = 0  # 暂无
        self.chm = 0  # 计算Function的
        self.chd = 0  # 计算Function的
        self.DSM = 0
        self.NOI = 0
        self.NOID = 0
        self.struct = dict()
        self.function = dict()
        self.__set_children()

    def __set_children(self):
        for cld in self.__children:
            self.DSM += 1
            if self.__vars_info[cld]['category'] == 'Struct':
                self.struct[self.__vars_info[cld]['qualifiedName']] = Class(cld, self.__vars_info, self.__children,
                                                                            self.__dep['class'])
            if self.__vars_info[cld]['category'] == 'Function':
                self.function[self.__vars_info[cld]['qualifiedName']] = Method(cld, self.__vars_info, self.__children,
                                                                               self.__dep['method'])
        self.__set_others()

    def __set_others(self):
        self.NOI = len(self.__dep['module'][self.__cur_module]) if self.__cur_module in self.__dep['module'] else 0
        self.__set_NOID()
        self.__set_rel()

    #     self.__set_cmt()
    #
    # def __set_cmt(self):
    #     # measure history dep
    #     focus_dic, spread_dic, module_classes, commit = get_spread_and_focus(cmt_path, package_info, variables)
    #     icf_dic, ecf_dic, rei_dic = get_icf_ecf_rei(module_classes, commit)

    def __set_NOID(self):
        for mod1 in self.__dep['module']:
            if self.__cur_module in self.__dep['module'][mod1]:
                self.NOID += 1

    def __set_rel(self):
        # 本file内所有一等公民(struct/function...)都要考虑
        self.__com_call_coh(self.__children, self.__dep, self.__vars_info)
        self.__com_call_coup(self.__cur_module, self.__all_contain, self.__dep, self.__vars_info)

    def __com_call_coh(self, children_id, dep_info, vars_info):
        struct_dep = dep_info['class']
        function_dep = dep_info['method']
        function_typeuse_dep = function_dep['typeuse_dep']
        function_call_dep = function_dep['call_dep']
        has_connections = 0
        all_connections = len(children_id) * len(children_id)
        if all_connections == 0:
            return
        for id1 in children_id:
            for id2 in children_id:
                if id1 != id2:
                    if vars_info[id1]['category'] == 'Struct':
                        if id1 in struct_dep and id2 in struct_dep[id1] and struct_dep[id1][id2] != 0:
                            has_connections += 1
                    if vars_info[id1]['category'] == 'Function':
                        if (id1 in function_typeuse_dep and id2 in function_typeuse_dep[id1] and
                            function_typeuse_dep[id1][id2]) != 0 or (
                                id1 in function_call_dep and id2 in function_call_dep[id1] and
                                function_call_dep[id1][id2]) != 0:
                            has_connections += 1
        self.scoh = has_connections / all_connections

    def __com_call_coup(self, current_module, module_info, dep_info, vars_info):
        if current_module not in module_info:
            return
        struct_dep = dep_info['class']
        function_dep = dep_info['method']
        function_typeuse_dep = function_dep['typeuse_dep']
        function_call_dep = function_dep['call_dep']
        scop = 0
        idd_list = list()
        odd_list = list()
        for module in module_info:
            if module != current_module:
                has_connections = 0
                current_module_odd = 0
                current_module_idd = 0
                for id1 in module_info[current_module]:
                    current_class_odd = 0
                    current_class_idd = 0
                    for id2 in module_info[module]:
                        if vars_info[id1]['category'] == 'Struct':
                            if id1 in struct_dep and id2 in struct_dep[id1] and struct_dep[id1][id2] != 0:
                                current_class_odd += 1
                                has_connections += 1
                            elif id2 in struct_dep and id1 in struct_dep[id2] and struct_dep[id2][id1] != 0:
                                current_class_idd += 1
                                has_connections += 1
                        if vars_info[id1]['category'] == 'Function':
                            if (id1 in function_typeuse_dep and id2 in function_typeuse_dep[id1] and
                                function_typeuse_dep[id1][id2]) != 0 or (
                                    id1 in function_call_dep and id2 in function_call_dep[id1] and
                                    function_call_dep[id1][id2]) != 0:
                                current_class_odd += 1
                                has_connections += 1
                            elif (id2 in function_typeuse_dep and id1 in function_typeuse_dep[id2] and
                                  function_typeuse_dep[id2][id1]) != 0 or (
                                    id2 in function_call_dep and id1 in function_call_dep[id2] and
                                    function_call_dep[id2][id1]) != 0:
                                current_class_idd += 1
                                has_connections += 1
                    current_module_odd += current_class_odd
                    current_module_idd += current_class_idd
                if current_module_odd != 0:
                    odd_list.append(1)
                else:
                    odd_list.append(0)
                if current_module_idd != 0:
                    idd_list.append(1)
                else:
                    idd_list.append(0)
                # 此处考虑在计算依赖时，应该是有向图，所以*2
                scop += has_connections / (2 * len(module_info[current_module]) * len(module_info[module]))
        self.scop = scop
        self.odd = sum(odd_list) / (len(module_info) - 1)
        self.idd = sum(idd_list) / (len(module_info) - 1)


class Project:
    def __init__(self, var_id_to_var, pro_info, out_path):
        self.version = pro_info['version']
        self.__out_path = out_path
        self.__vars_info = var_id_to_var
        self.__contain = pro_info['contain']
        self.__dep = pro_info['dep']
        self.score = 0
        self.SMQ = 0
        self.ODD = 0
        self.IDD = 0
        self.SPREAD = 0  # 暂无
        self.FOCUS = 0  # 暂无
        self.ICF = 0  # 暂无
        self.ICF = 0  # 暂无
        self.ECF = 0  # 暂无
        self.REI = 0  # 暂无
        self.CHM = 0
        self.CHD = 0
        self.module = dict()
        self.__set_module()
        # self.__set_others()
        # __set_score(self.)
        self.__to_csv()

    def __set_module(self):
        # tmp_class_contain = dict()
        # for mod in self.__contain:
        #     for child in self.__contain[mod]:
        #         if self.__vars_info[child]['category'] == 'Struct':
        #             if mod not in tmp_class_contain:
        #                 tmp_class_contain[mod] = list()
        #             tmp_class_contain[mod].append(child)
        for mod in self.__contain:
            self.module[self.__vars_info[mod]['qualifiedName']] = Module(mod, self.__vars_info, self.__contain,
                                                                         self.__dep)

    # def __set_others(self):
    #     self.__set_cmt()

    def __to_csv(self):
        # 获取所有可能的列名
        fieldnames1 = list()
        # for row1 in self:
        # fieldnames1.update('version')
        fieldnames1.append('score')
        fieldnames1.extend(PROJECT_METRICS)
        fieldnames1.append('module')
        fieldnames1.extend(MODULE_METRICS)
        fieldnames1.append('class')
        fieldnames1.extend(CLASS_METRICS)
        fieldnames2 = list()
        fieldnames2.append('module')
        fieldnames2.append('method')
        fieldnames2.extend(METHOD_METRICS)

        # 计算project指标
        tmp_metrics = list()
        for row1 in self.module:
            tmp_metrics.append(list(itemgetter(*MODULE_METRICS)(self.__get__all_attrs(self.module[row1]))))
        result = list()
        for item in tmp_metrics:
            temp = [item[0] - item[1]]
            temp.extend(item[2: 11: 1])
            result.append(temp)
        project_metrics = np.around(np.array(result).mean(axis=0).tolist(), 4)
        [normalized_result, score_result] = get_score(tmp_metrics,
                                                      [[0.08], [0.08], [0.07], [0.07], [0.07], [0.07], [0.07], [0.07],
                                                       [0.07], [0.07], [0.07], [0.07], [0.07], [0.07]],
                                                      MODULE_METRICS)
        project_metrics = np.insert(project_metrics, 0, np.mean(score_result))
        # 将数据写入CSV文件
        with open('output1.csv', 'w', newline='') as csvfile:
            writer1 = csv.writer(csvfile, delimiter=",")
            row_data = list()
            row_data.append(fieldnames1)
            for row1 in self.module:
                for row2 in self.module[row1].struct:
                    tmp = list(project_metrics)
                    tmp.append(row1)
                    tmp.extend(list(itemgetter(*MODULE_METRICS)(self.__get__all_attrs(self.module[row1]))))
                    tmp.append(row2)
                    tmp.extend(list(itemgetter(*CLASS_METRICS)(self.__get__all_attrs(self.module[row1].struct[row2]))))
                    row_data.append(tmp)
            writer1.writerows(row_data)

        with open('output2.csv', 'w', newline='') as csvfile:
            writer2 = csv.writer(csvfile, delimiter=",")
            row_data = list()
            row_data.append(fieldnames2)
            for row1 in self.module:
                for row2 in self.module[row1].function:
                    tmp = list()
                    tmp.append(row1)
                    # tmp.extend(list(itemgetter(*MODULE_METRICS)(self.__get__all_attrs(self.module[row1]))))
                    tmp.append(row2)
                    tmp.extend(
                        list(itemgetter(*METHOD_METRICS)(self.__get__all_attrs(self.module[row1].function[row2]))))
                    row_data.append(tmp)
            writer2.writerows(row_data)

    def __get__all_attrs(self, obj):
        attrs = dict()
        for o in dir(obj):
            attrs[o] = getattr(obj, o)
        return attrs
    #
    # def __set_cmt(self):
    #     cmt_path = os.path.join(self.__out_path, 'cmt.csv')
    #     # measure history dep
    #     focus_dic, spread_dic, module_classes, commit = get_spread_and_focus(cmt_path, self.__contain, self.__vars_info)
    #     icf_dic, ecf_dic, rei_dic = get_icf_ecf_rei(module_classes, commit)
