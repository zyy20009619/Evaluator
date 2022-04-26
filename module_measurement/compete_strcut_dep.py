
def com_struct_metric(variables, current_module, module_info, struct_dep, method_class, call):
    scoh, idcc_list = com_call_coh(module_info[current_module], struct_dep)
    scop, odd, idd, edcc_list = com_call_coup(variables, current_module, module_info, struct_dep)
    return scoh, scop, odd, idd, idcc_list, edcc_list


def com_call_coh(classes_id, struct_dep):
    # count the IDCC
    idcc_list = dict()
    has_connections = 0
    all_connections = len(classes_id) * len(classes_id)
    for id1 in classes_id:
        current_class_odd = 0
        current_class_idd = 0
        for id2 in classes_id:
            if id1 != id2:
                if id1 in struct_dep and id2 in struct_dep[id1] and struct_dep[id1][id2] != 0:
                    has_connections += 1
                    current_class_odd += 1
                elif id2 in struct_dep and id1 in struct_dep[id2] and struct_dep[id2][id1] != 0:
                    current_class_idd += 1
        if id1 not in idcc_list:
            idcc_list[id1] = 0
        idcc_list[id1] += current_class_odd + current_class_idd
    scoh = has_connections / all_connections
    return scoh, idcc_list


def com_call_coup(variables, current_module, module_info, struct_dep):
    scop = 0
    idd_list = list()
    odd_list = list()
    edcc_list = dict()
    for module in module_info:
        # when '!=', count the EDCC
        if module != current_module:
            has_connections = 0
            current_module_odd = 0
            current_module_idd = 0
            for id1 in module_info[current_module]:
                current_class_odd = 0
                current_class_idd = 0
                for id2 in module_info[module]:
                    if id1 in struct_dep and id2 in struct_dep[id1] and struct_dep[id1][id2] != 0:
                        current_class_odd += 1
                        has_connections += 1
                    elif id2 in struct_dep and id1 in struct_dep[id2] and struct_dep[id2][id1] != 0:
                        current_class_idd += 1
                        has_connections += 1
                if id1 not in edcc_list:
                    edcc_list[id1] = 0
                edcc_list[id1] += current_class_odd + current_class_idd
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

            scop += has_connections / (2 * len(module_info[current_module]) * len(module_info[module]))
    return scop, sum(odd_list) / (len(module_info) - 1), sum(idd_list) / (len(module_info) - 1), edcc_list