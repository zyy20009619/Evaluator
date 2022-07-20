from util.json_operator import read_folder, write_result_to_json
from util.csv_operator import write_to_csv
from detect_algo.arch_debt.measure_arch import measure_maintenance
import os
import csv
import matplotlib.pyplot as plt


def analyse_data(diff_folder_path, project_path):
    measure_diff, dep_diff = read_folder(diff_folder_path, 'measure_diff.json', 'dep_diff.json')
    if not (measure_diff or dep_diff or os.path.exists(project_path)):
        return False
    _scan_problems(diff_folder_path, measure_diff, dep_diff, project_path)
    return True


def _scan_problems(diff_folder_path, measure_diff, dep_diff, project_path):
    all_causes = dict()
    coupling_dic = dict()
    functionality_list = list()
    modularity_list = list()
    evolution_list = list()
    sort_dic = dict()
    causes_entities = list()
    causes_to_entities = dict()
    flag = 0
    for diff_module_name in measure_diff:
        # problem4: find functionality problems at the class-level
        _find_causes_at_functionality(measure_diff[diff_module_name]['classes'], functionality_list, causes_entities,
                                      causes_to_entities)
        # problem1: δscop>0
        if float(measure_diff[diff_module_name]['scop']) > 0:
            flag += 1
            # root cause1: the number of coupling ↑
            # is_coupling_num = False
            # if float(measure_diff[diff_module_name]['odd']) > 0 or float(measure_diff[diff_module_name]['idd']) > 0:
            #     is_coupling_num = True
            inherit_entities, call_entities, import_entities = _scan_causes_at_class(
                measure_diff[diff_module_name]['classes'], dep_diff,
                causes_entities, causes_to_entities)
            if len(inherit_entities) != 0 or len(call_entities) != 0 or len(import_entities) != 0:
                coupling_dic[diff_module_name] = {'inherit': inherit_entities,
                                                  'call': call_entities,
                                                  'import': import_entities}
                sort_dic[diff_module_name] = float(measure_diff[diff_module_name]['scop'])
        # problem2: δ rei>0
        if float(measure_diff[diff_module_name]['rei']) > 0 and (
                float(measure_diff[diff_module_name]['ecf']) > 0 or float(measure_diff[diff_module_name]['icf']) < 0):
            evolution_list.append(diff_module_name)
        # problem3: δ spread>0 ∧ δ focus<0
        if float(measure_diff[diff_module_name]['spread']) > 0 and float(measure_diff[diff_module_name]['focus']) < 0:
            modularity_list.append(diff_module_name)
    # temp count
    inherit_count = 0
    call_count = 0
    import_count = 0
    for module in coupling_dic:
        if len(coupling_dic[module]['inherit']) != 0:
            inherit_count += 1
        if len(coupling_dic[module]['call']) != 0:
            call_count += 1
        if len(coupling_dic[module]['import']) != 0:
            import_count += 1
    test_module = list()
    test_module.extend(list(coupling_dic.keys()))
    test_module.extend(list(modularity_list))
    test_module.extend(list(evolution_list))
    test_module = list(set(test_module))

    # sort coupling_dic by scop
    coupling_dic = _sort_coupling_dic(coupling_dic, sort_dic)
    all_causes['coupling'] = coupling_dic
    all_causes['functionality'] = list(set(functionality_list))
    all_causes['modularity'] = modularity_list
    all_causes['evolution'] = evolution_list

    # print('coupling module count', len(list(set(coupling_dic.keys()))))
    # print('modular module count', len(list(set(modularity_list))))
    # print('evolution module count', len(list(set(evolution_list))))
    # print('union module count', len(list(set(test_module))))
    # print('diff module count', len(measure_diff))
    # print('scop count', flag)

    write_result_to_json(os.path.join(diff_folder_path, 'causes.json'), all_causes)
    # causes_entities: a list of error-prone classes
    [version_list, causes_cmt_mc_list, causes_change_loc_mc_list, causes_author_mc_list, causes_issue_mc_list,
     causes_issue_cmt_mc_list, causes_issue_loc_mc_list, cmt_list, change_loc_list, author_list, issue_list,
     issue_cmt_list, issue_loc_list, all_files_mc_dic] = measure_maintenance(project_path,
                                                                             list(set(causes_entities)),
                                                                             causes_to_entities)
    _count_files_anti_patterns(causes_to_entities, all_files_mc_dic)
    # _column_chart(version_list, cmt_list, 'cmt')
    # _column_chart(version_list, change_loc_list, 'change_loc')
    # _column_chart(version_list, author_list, 'author')
    # _column_chart(version_list, issue_list, 'issue')
    # _column_chart(version_list, issue_cmt_list, 'issue_cmt')
    # _column_chart(version_list, issue_loc_list, 'issue_loc')
    # _line_chart(version_list, causes_cmt_mc_list, 'cmt')
    # _line_chart(version_list, causes_change_loc_mc_list, 'change_loc')
    # _line_chart(version_list, causes_author_mc_list, 'author')
    # _line_chart(version_list, causes_issue_mc_list, 'issue')
    # _line_chart(version_list, causes_issue_cmt_mc_list, 'issue_cmt')
    # _line_chart(version_list, causes_issue_loc_mc_list, 'issue_loc')
    # model_selector(version_list, [j[1] for j in coupling_mc_list])
    #
    # # 每种现象拟合一条回归曲线（暂时使用散点图表示）
    # _fit_mc_curve(version_list, _com_percentage_of_other_metrics([j[0] for j in coupling_mc_list], author_list),
    #               'coupling_author')
    # _fit_mc_curve(version_list, _com_percentage_of_other_metrics([j[1] for j in coupling_mc_list], cmt_list),
    #               'coupling_cmt')
    # _fit_mc_curve(version_list, _com_percentage_of_loc([j[2] for j in coupling_mc_list], change_loc_list),
    #               'coupling_changeloc')
    # _fit_mc_curve(version_list, _com_percentage_of_other_metrics([j[3] for j in coupling_mc_list], issue_list),
    #               'coupling_issue')
    # _fit_mc_curve(version_list, [j[4] for j in coupling_mc_list], 'coupling_issue-cmt')
    # _fit_mc_curve(version_list, [j[5] for j in coupling_mc_list], 'coupling_issueLoc')
    # _fit_mc_curve(version_list, _com_percentage_of_other_metrics([j[0] for j in functionality_mc_list], author_list),
    #               'functionality_author')
    # _fit_mc_curve(version_list, _com_percentage_of_other_metrics([j[1] for j in functionality_mc_list], cmt_list),
    #               'functionality_cmt')
    # _fit_mc_curve(version_list, _com_percentage_of_loc([j[2] for j in functionality_mc_list], change_loc_list),
    #               'functionality_changeloc')
    # _fit_mc_curve(version_list, _com_percentage_of_other_metrics([j[3] for j in functionality_mc_list], issue_list),
    #               'functionality_issue')
    # _fit_mc_curve(version_list, [j[4] for j in functionality_mc_list], 'functionality_issue-cmt')
    # _fit_mc_curve(version_list, [j[5] for j in functionality_mc_list], 'functionality_issueLoc')


def _count_files_anti_patterns(causes_to_entities, all_files_mc_dic):
    res_files = dict()
    res_files_root_causes = dict()

    _append_num(res_files, res_files_root_causes, list(set(causes_to_entities['inherit'])), 'coupling-inherit')
    _append_num(res_files, res_files_root_causes, list(set(causes_to_entities['call'])), 'coupling-call')
    _append_num(res_files, res_files_root_causes, list(set(causes_to_entities['import'])), 'coupling-import')
    _append_num(res_files, res_files_root_causes, list(set(causes_to_entities['functionality'])), 'functionality')

    res_files = sorted(res_files.items(), key=lambda x: x[1], reverse=True)

    res = list()
    res.append(
        ['filename', 'number of anti-patterns', 'anti-patterns', 'author', 'cmt', 'change loc', 'issue', 'issue cmt',
         'issue loc'])
    for file in res_files:
        for file_mc in all_files_mc_dic:
            if file[0].replace('.', '\\') in file_mc:
                res.append([file[0], file[1], ','.join(res_files_root_causes[file[0]]),
                            str(len(set(all_files_mc_dic[file_mc]['author_id']))),
                            str(len(set(all_files_mc_dic[file_mc]['cmt_id']))),
                            str(all_files_mc_dic[file_mc]['change_loc']), str(len(set(all_files_mc_dic[file_mc]['issue_id']))),
                            str(len(set(all_files_mc_dic[file_mc]['issue_cmt_id']))),
                            str(all_files_mc_dic[file_mc]['issue_loc'])])
                break
    os.chdir(r'C:\Users\20465\Desktop\codes\MicroEvaluator')
    write_to_csv(res, 'files_ap.csv')


def _append_num(files_dic, res_files_root_causes, classes_list, cause):
    for c in classes_list:
        if c not in files_dic:
            files_dic[c] = 0
            res_files_root_causes[c] = list()
        files_dic[c] += 1
        res_files_root_causes[c].append(cause)


def _column_chart(version_list, issue_list, title):
    x = list(range(len(issue_list)))
    total_width, n = 0.8, 2
    width = total_width / n
    plt.bar(x, [j[0] for j in issue_list], width=width, label='avg_pf_mc')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, [j[1] for j in issue_list], width=0.4, label='avg_non_pf_mc', tick_label=version_list)
    plt.legend()
    plt.title(title)
    plt.show()


def _line_chart(version_list, causes_mc_list, title):
    plt.plot(version_list, [j[0] for j in causes_mc_list], 'b*--', alpha=0.5, linewidth=1, label='coupling-inherit')
    plt.plot(version_list, [j[1] for j in causes_mc_list], 'rs--', alpha=0.5, linewidth=1, label='coupling-call')
    plt.plot(version_list, [j[2] for j in causes_mc_list], 'go--', alpha=0.5, linewidth=1, label='coupling-import')
    plt.plot(version_list, [j[3] for j in causes_mc_list], 'gx--', alpha=0.5, linewidth=1, label='functionality')

    # for a, b1 in zip(version_list, [j[0] for j in causes_mc_list]):
    #     plt.text(a, b1, str(b1), ha='center', va='bottom', fontsize=8)
    # for a, b2 in zip(version_list, [j[1] for j in causes_mc_list]):
    #     plt.text(a, b2, str(b2), ha='center', va='bottom', fontsize=8)
    # for a, b3 in zip(version_list, [j[2] for j in causes_mc_list]):
    #     plt.text(a, b3, str(b3), ha='center', va='bottom', fontsize=8)
    # for a, b4 in zip(version_list, [j[3] for j in causes_mc_list]):
    #     plt.text(a, b4, str(b4), ha='center', va='bottom', fontsize=8)
    plt.legend()
    plt.title(title)
    plt.xlabel('version')
    plt.ylabel('maintenance cost')

    plt.show()


def _com_percentage_of_other_metrics(one_count_list, all_count_list):
    res_list = list()
    for index in range(0, len(all_count_list)):
        res_list.append(one_count_list[index] / len(all_count_list[index]))
    return res_list


def _com_percentage_of_loc(one_count_list, all_count_list):
    res_list = list()
    for index in range(0, len(all_count_list)):
        res_list.append(one_count_list[index] / all_count_list[index])
    return res_list


def _fit_mc_curve(version_list, mc_list, title_name):
    plt.title(title_name, fontsize=24)
    plt.xlabel("versions", fontsize=14)
    plt.ylabel("maintenance_cost", fontsize=14)

    plt.axis([0, len(version_list), 0, max(mc_list)])
    plt.scatter(version_list, mc_list, c='red', edgecolors='none', s=20)
    plt.show()


def _sort_coupling_dic(coupling_dic, sort_dic):
    sorted_coupling_dic = dict()
    sort_dic_tuple = sorted(sort_dic.items(), key=lambda x: x[1], reverse=True)
    for tuple in sort_dic_tuple:
        sorted_coupling_dic[tuple[0]] = coupling_dic[tuple[0]]
    return sorted_coupling_dic


def _find_causes_at_functionality(classes_dic, functionality_list, causes_entities, causes_to_entities):
    for class_name in classes_dic:
        if float(classes_dic[class_name]['c_chm']) < 0 and float(classes_dic[class_name]['c_chd']) < 0:
            functionality_list.append(class_name)
            causes_entities.append(class_name)
            if 'functionality' not in causes_to_entities:
                causes_to_entities['functionality'] = list()
            causes_to_entities['functionality'].append(class_name)


def _scan_causes_at_class(classes_dic, dep_diff, causes_entities, causes_to_entities):
    inherit_entities = list()
    import_entities = list()
    call_entities = list()
    for class_name in classes_dic:
        if classes_dic[class_name]['CBC'] > 0 and classes_dic[class_name]['EDCC'] > 0 and classes_dic[class_name][
            'IDCC'] <= 0:
            # root cause1: by inherit
            if classes_dic[class_name]['c_FAN_OUT'] > 0 and classes_dic[class_name]['NAC'] > 0:
                if class_name in dep_diff['inherit']:
                    inherit_entities.append(
                        {'src': class_name, 'dest': dep_diff['inherit'][class_name], 'type': 'inherit'})
                    causes_entities.append(class_name)
                    if 'inherit' not in causes_to_entities:
                        causes_to_entities['inherit'] = list()
                    causes_to_entities['inherit'].append(class_name)
            if classes_dic[class_name]['c_FAN_IN'] > 0 and classes_dic[class_name]['NDC'] > 0:
                if class_name in dep_diff['descendent']:
                    inherit_entities.append(
                        {'src': class_name, 'dest': dep_diff['descendent'][class_name], 'type': 'descendent'})
                    causes_entities.append(class_name)
                    if 'inherit' not in causes_to_entities:
                        causes_to_entities['inherit'] = list()
                    causes_to_entities['inherit'].append(class_name)

            # root cause2: by import
            if classes_dic[class_name]['c_FAN_OUT'] > 0 and classes_dic[class_name]['NOI'] > 0:
                if class_name in dep_diff['import']:
                    import_entities.append(
                        {'src': class_name, 'dest': dep_diff['import'][class_name], 'type': 'import'})
                    causes_entities.append(class_name)
                    if 'import' not in causes_to_entities:
                        causes_to_entities['import'] = list()
                    causes_to_entities['import'].append(class_name)
            if classes_dic[class_name]['c_FAN_OUT'] > 0 and classes_dic[class_name]['NOID'] > 0:
                if class_name in dep_diff['imported']:
                    import_entities.append(
                        {'src': class_name, 'dest': dep_diff['imported'][class_name], 'type': 'imported'})
                    causes_entities.append(class_name)
                    if 'import' not in causes_to_entities:
                        causes_to_entities['import'] = list()
                    causes_to_entities['import'].append(class_name)

            # root cause3: by method invoke
            for method_name in classes_dic[class_name]['methods']:
                if classes_dic[class_name]['methods'][method_name]['CBM'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['EDMC'] > 0 and \
                        classes_dic[class_name]['methods'][method_name]['IDMC'] <= 0:
                    if classes_dic[class_name]['c_FAN_OUT'] > 0 and \
                            classes_dic[class_name]['methods'][method_name]['m_FAN_OUT'] > 0:
                        if method_name in dep_diff['call']:
                            call_entities.append(
                                {'src': method_name, 'dest': dep_diff['call'][method_name], 'type': 'call'})
                            causes_entities.append(class_name)
                            if 'call' not in causes_to_entities:
                                causes_to_entities['call'] = list()
                            causes_to_entities['call'].append(class_name)
                    if classes_dic[class_name]['c_FAN_IN'] > 0 and \
                            classes_dic[class_name]['methods'][method_name]['m_FAN_IN'] > 0:
                        if method_name in dep_diff["called"]:
                            call_entities.append(
                                {'src': method_name, 'dest': dep_diff['called'][method_name], 'type': 'called'})
                            causes_entities.append(class_name)
                            if 'call' not in causes_to_entities:
                                causes_to_entities['call'] = list()
                            causes_to_entities['call'].append(class_name)

    return inherit_entities, call_entities, import_entities
