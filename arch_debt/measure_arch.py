from arch_debt.maintenance_cost_measurement.changeproness import *
from arch_debt.maintenance_cost_measurement.gitlogprocessor import *
from util.csv_operator import write_to_csv, read_csv, read_csv_to_pd


def com_mc(project_path, vers, cause_path, out_path):
    # causes_entities = read_csv(cause_path, 'causes_entities.csv')
    causes_entities = read_csv_to_pd(cause_path, 'causes_entities.csv')
    measure_maintenance(project_path, list(set(causes_entities.iloc[:, -1])), vers, out_path)


def measure_maintenance(project_path, causes_entities, vers, out_path):
    # coupling_mc_list = list()
    # functionality_mc_list = list()
    causes_cmt_mc_list = list()
    causes_author_mc_list = list()
    causes_issue_mc_list = list()
    causes_issue_cmt_mc_list = list()
    causes_issue_loc_mc_list = list()
    causes_change_loc_mc_list = list()
    cmt_list = list()
    change_loc_list = list()
    author_list = list()
    issue_list = list()
    issue_cmt_list = list()
    issue_loc_list = list()

    versions = vers.split('?')
    for version in versions:
        os.system('git checkout -f ' + version)
        # all commits infos
        mc_file, file_list_java, file_loc_dict = gitlog(project_path, version, out_path)
        # all files mc
        out_file = out_path + '/mc/' + version + '/file-mc.csv'
        all_files_mc_dic = changeProness(file_list_java, mc_file, out_file)
        # compete different causes mc
        com_causes_mc(all_files_mc_dic, file_loc_dict, causes_entities,
                                  causes_cmt_mc_list, causes_change_loc_mc_list, causes_author_mc_list,
                                  causes_issue_mc_list,
                                  causes_issue_cmt_mc_list, causes_issue_loc_mc_list, cmt_list, change_loc_list,
                                  author_list,
                                  issue_list, issue_cmt_list, issue_loc_list)
    write_to_csv(cmt_list, out_path + '/mc/causes_cmt.csv')
    write_to_csv(change_loc_list, out_path + '/mc/causes_change_loc.csv')
    write_to_csv(author_list, out_path + '/mc/causes_author.csv')
    write_to_csv(issue_list, out_path + '/mc/causes_issue.csv')
    write_to_csv(issue_cmt_list, out_path + '/mc/causes_issue_cmt.csv')
    write_to_csv(issue_loc_list, out_path + '/mc/causes_issue_loc.csv')
    # return author_list, cmt_list, change_loc_list, issue_list


def com_causes_mc(all_files_mc_dic, file_loc_dict, causes_entities, causes_cmt_mc_list,
                  causes_change_loc_mc_list, causes_author_mc_list, causes_issue_mc_list,
                  causes_issue_cmt_mc_list, causes_issue_loc_mc_list,
                  cmt_list, change_loc_list, author_list, issue_list, issue_cmt_list,
                  issue_loc_list):
    causes_mc_result = list()
    causes_mc_result.append(['cause', '#author', '#cmt', '#changeloc', '#issue', '#issue-cmt', 'issueLoc'])
    # test_entities = list()
    new_causes_entities = _format_file_path(all_files_mc_dic, causes_entities)

    non_causes_entities_cmt = list()
    non_causes_entities_change_loc = 0
    non_causes_entities_author = list()
    non_causes_entities_issue_cmt = list()
    non_causes_entities_issue_loc = 0
    non_causes_entities_issue = list()
    non_causes_entities = set(list(all_files_mc_dic.keys())) - set(list(new_causes_entities.keys()))
    non_causes_entity_loc_num = 0
    for non_causes_entity in non_causes_entities:
        if non_causes_entity.replace('\\', '/') in file_loc_dict:
            non_causes_entity_loc_num += int(file_loc_dict[non_causes_entity.replace('\\', '/')])
            non_causes_entities_cmt.extend(all_files_mc_dic[non_causes_entity]['cmt_id'])
            non_causes_entities_change_loc += all_files_mc_dic[non_causes_entity]['change_loc']
            non_causes_entities_author.extend(all_files_mc_dic[non_causes_entity]['author_id'])
            non_causes_entities_issue_cmt.extend(all_files_mc_dic[non_causes_entity]['issue_cmt_id'])
            non_causes_entities_issue_loc += all_files_mc_dic[non_causes_entity]['issue_loc']
            non_causes_entities_issue.extend(all_files_mc_dic[non_causes_entity]['issue_id'])

    causes_entities_cmt = list()
    causes_entities_change_loc = 0
    causes_entities_author = list()
    causes_entities_issue_cmt = list()
    causes_entities_issue_loc = 0
    causes_entities_issue = list()
    causes_entity_loc_num = 0
    for cause_entity in new_causes_entities:
        if cause_entity.replace('\\', '/') in file_loc_dict:
            causes_entity_loc_num += int(file_loc_dict[cause_entity.replace('\\', '/')])
            causes_entities_cmt.extend(all_files_mc_dic[cause_entity]['cmt_id'])
            causes_entities_change_loc += all_files_mc_dic[cause_entity]['change_loc']
            causes_entities_author.extend(all_files_mc_dic[cause_entity]['author_id'])
            causes_entities_issue_cmt.extend(all_files_mc_dic[cause_entity]['issue_cmt_id'])
            causes_entities_issue_loc += all_files_mc_dic[cause_entity]['issue_loc']
            causes_entities_issue.extend(all_files_mc_dic[cause_entity]['issue_id'])

    issue_list.append(['causes_mc', 'no_causes_mc'])
    issue_list.append([len(set(causes_entities_issue)) / causes_entity_loc_num,
                       len(set(non_causes_entities_issue)) / non_causes_entity_loc_num])
    cmt_list.append(['causes_mc', 'no_causes_mc'])
    cmt_list.append([len(set(causes_entities_cmt)) / causes_entity_loc_num,
                     len(set(non_causes_entities_cmt)) / non_causes_entity_loc_num])
    change_loc_list.append(['causes_mc', 'no_causes_mc'])
    change_loc_list.append([causes_entities_change_loc / causes_entity_loc_num,
                            non_causes_entities_change_loc / non_causes_entity_loc_num])
    author_list.append(['causes_mc', 'no_causes_mc'])
    author_list.append([len(set(causes_entities_author)) / causes_entity_loc_num,
                        len(set(non_causes_entities_author)) / non_causes_entity_loc_num])
    issue_cmt_list.append(['causes_mc', 'no_causes_mc'])
    issue_cmt_list.append([len(set(causes_entities_issue_cmt)) / causes_entity_loc_num,
                           len(set(non_causes_entities_issue_cmt)) / non_causes_entity_loc_num])
    issue_loc_list.append(['causes_mc', 'no_causes_mc'])
    issue_loc_list.append([causes_entities_issue_loc / causes_entity_loc_num,
                           non_causes_entities_issue_loc / non_causes_entity_loc_num])
    #
    # for cause in causes_to_entities:
    #     author = list()
    #     cmt = list()
    #     change_loc = 0
    #     issue = list()
    #     issue_cmt = list()
    #     issue_loc = 0
    #     one_entities_list = list(set(causes_to_entities[cause]))
    #     loc_num = 0
    #     for entity in one_entities_list:
    #         for file in all_files_mc_dic:
    #             if entity.replace('.', '\\') in file:
    #                 loc_num += int(file_loc_dict[file.replace('\\', '/')])
    #                 author.extend(all_files_mc_dic[file]['author_id'])
    #                 cmt.extend(all_files_mc_dic[file]['cmt_id'])
    #                 change_loc += all_files_mc_dic[file]['change_loc']
    #                 issue.extend(all_files_mc_dic[file]['issue_id'])
    #                 issue_cmt.extend(all_files_mc_dic[file]['issue_cmt_id'])
    #                 issue_loc += all_files_mc_dic[file]['issue_loc']
    #                 break
    #     if cause == 'inherit':
    #         inherit_cmt_mc = len(set(cmt)) / loc_num
    #         inherit_change_loc_mc = change_loc / loc_num
    #         inherit_author_mc = len(set(author)) / loc_num
    #         inherit_issue_mc = len(set(issue)) / loc_num
    #         inherit_issue_cmt_mc = len(set(issue_cmt)) / loc_num
    #         inherit_issue_loc_mc = issue_loc / loc_num
    #     if cause == 'call':
    #         call_cmt_mc = len(set(cmt)) / loc_num
    #         call_change_loc_mc = change_loc / loc_num
    #         call_author_mc = len(set(author)) / loc_num
    #         call_issue_mc = len(set(issue)) / loc_num
    #         call_issue_cmt_mc = len(set(issue_cmt)) / loc_num
    #         call_issue_loc_mc = issue_loc / loc_num
    #     if cause == 'import':
    #         import_cmt_mc = len(set(cmt)) / loc_num
    #         import_change_loc_mc = change_loc / loc_num
    #         import_author_mc = len(set(author)) / loc_num
    #         import_issue_mc = len(set(issue)) / loc_num
    #         import_issue_cmt_mc = len(set(issue_cmt)) / loc_num
    #         import_issue_loc_mc = issue_loc / loc_num
    #     if cause == 'functionality':
    #         functionality_cmt_mc = len(set(cmt)) / loc_num
    #         functionality_change_loc_mc = change_loc / loc_num
    #         functionality_author_mc = len(set(author)) / loc_num
    #         functionality_issue_mc = len(set(issue)) / loc_num
    #         functionality_issue_cmt_mc = len(set(issue_cmt)) / loc_num
    #         functionality_issue_loc_mc = issue_loc / loc_num
    #
    #     causes_mc_result.append(
    #         [cause, len(set(author)), len(set(cmt)), change_loc, len(set(issue)), len(set(issue_cmt)), issue_loc])
    # causes_cmt_mc_list.append([inherit_cmt_mc, call_cmt_mc, import_cmt_mc, functionality_cmt_mc])
    # causes_change_loc_mc_list.append(
    #     [inherit_change_loc_mc, call_change_loc_mc, import_change_loc_mc, functionality_change_loc_mc])
    # causes_author_mc_list.append(
    #     [inherit_author_mc, call_author_mc, import_author_mc, functionality_author_mc])
    # causes_issue_mc_list.append(
    #     [inherit_issue_mc, call_issue_mc, import_issue_mc, functionality_issue_mc])
    # causes_issue_cmt_mc_list.append(
    #     [inherit_issue_cmt_mc, call_issue_cmt_mc, import_issue_cmt_mc, functionality_issue_cmt_mc])
    # causes_issue_loc_mc_list.append(
    #     [inherit_issue_loc_mc, call_issue_loc_mc, import_issue_loc_mc, functionality_issue_loc_mc])
    # return causes_mc_result


def _format_file_path(all_files_mc_dic, causes_entities):
    result = dict()
    for causes_entity in causes_entities:
        for file in all_files_mc_dic:
            if causes_entity.replace('.', '\\') in file:
                result[file] = causes_entity
                break
    return result