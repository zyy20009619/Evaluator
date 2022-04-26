
def count_method_and_var(variables, contain, inherit, descendent, method_class, call, idcc_list, edcc_list, override):
    class_dic = dict()
    for c in contain:
        dic_id = contain[c]
        CIS = 0
        NOM = 0
        CTM = 0
        NOP = 0
        var_num = 0
        private_var_num = 0
        for id in dic_id:
            if 'accessibility' in variables[id]:
                if variables[id]['category'] == 'Method':
                    NOM += 1
                    if id in call:
                        for call_id in call[id]:
                            if method_class[call_id] != c:
                                CTM += 1
                    if id in override:
                        NOP += 1
                    if variables[id]['accessibility'] == 'Public':
                        CIS += 1
                elif variables[id]['category'] == 'Variable':
                    if variables[id]['accessibility'] == 'Private':
                        private_var_num += 1
                    var_num += 1
        NAC = find_node_num(inherit, c, variables, 0)
        NDC = find_node_num(descendent, c, variables, 0)
        if var_num == 0:
            DAM = -1
        else:
            DAM = format(private_var_num / var_num, '.4f')

        class_dic[variables[c]['qualifiedName']] = {'CIS': CIS, 'NOM': NOM, 'NOP': NOP, 'NAC': NAC, 'NDC': NDC, 'CTM': CTM, 'DAM': DAM, 'IDCC': idcc_list[c], 'EDCC': edcc_list[c]}
    return class_dic


def find_node_num(rel_dic, class_id, variables, count):
    if class_id in rel_dic:
        count += len(rel_dic[class_id])
        for parent_id in rel_dic[class_id]:
            find_node_num(rel_dic, parent_id, variables, count)
    else:
        return 0
    return count
