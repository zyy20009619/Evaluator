import os

import pandas as pd

from arch_debt.maintenance_cost_measurement.changeproness import *
from arch_debt.maintenance_cost_measurement.gitlogprocessor import *
from util.csv_operator import write_to_csv, read_csv, read_csv_to_pd


def com_mc(project_path, vers, detect_path):
    # causes_entities = read_csv(cause_path, 'causes_entities.csv')
    detection_res = read_csv_to_pd(os.path.join(detect_path, 'detection result.csv'))
    measure_maintenance(project_path, list(set(detection_res['problem class'])), vers, detect_path)


def measure_maintenance(project_path, pf_entities, vers, detect_path):
    # causes_cmt_mc_list = list()
    # causes_author_mc_list = list()
    # causes_issue_mc_list = list()
    # causes_issue_cmt_mc_list = list()
    # causes_issue_loc_mc_list = list()
    # causes_change_loc_mc_list = list()
    # cmt_list = list()
    # change_loc_list = list()
    # author_list = list()
    # issue_list = list()
    # issue_cmt_list = list()
    # issue_loc_list = list()
    # issue_list.append(['mc(A)', 'avg_non_pf_mc'])
    # cmt_list.append(['avg_pf_mc', 'avg_non_pf_mc'])
    # change_loc_list.append(['avg_pf_mc', 'avg_non_pf_mc'])
    # author_list.append(['avg_pf_mc', 'avg_non_pf_mc'])
    # issue_cmt_list.append(['avg_pf_mc', 'avg_non_pf_mc'])
    # issue_loc_list.append(['avg_pf_mc', 'avg_non_pf_mc'])
    os.chdir(project_path)
    mc_list = list()
    versions = vers.split('?')
    for version in versions:
        version_mc = list()
        version_mc.append(version)
        base_version_path = os.path.join(detect_path, 'mc/' + version)
        # 获取到该版本的loc和log，计算版本中每个文件的维护成本
        commit_collection_res, file_list_java, file_loc_dict = gitlog(version, base_version_path)
        # 计算所有文件的维护成本
        all_files_mc_pd = changeProness(file_list_java, commit_collection_res,
                                        create_file_path(base_version_path, 'file mc.csv'))
        # 计算问题实体和非问题实体的维护成本
        com_pfs_mc(all_files_mc_pd, file_loc_dict, pf_entities, version_mc)
        mc_list.append(version_mc)
    res_pf = pd.DataFrame(data=mc_list, columns=['version', '#commit-mc(A)', '#commit-mc(B)', '#commit-average(P)',
                                                 '#changeLoc-mc(A)', '#changeLoc-mc(B)', '#changeLoc-average(P)',
                                                 '#author-mc(A)', '#author-mc(B)', '#author-average(P)'])
    res_pf['projectname'] = os.path.basename(project_path)
    res_pf.to_csv(os.path.join(detect_path, "mc result.csv"), index=False, sep=',')
    # write_to_csv(cmt_list, out_path + '/mc/causes_cmt.csv')
    # write_to_csv(change_loc_list, out_path + '/mc/causes_change_loc.csv')
    # write_to_csv(author_list, out_path + '/mc/causes_author.csv')
    # 切换回当前工作目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # write_to_csv(issue_list, out_path + '/mc/causes_issue.csv')
    # write_to_csv(issue_cmt_list, out_path + '/mc/causes_issue_cmt.csv')
    # write_to_csv(issue_loc_list, out_path + '/mc/causes_issue_loc.csv')


def com_pfs_mc(all_files_mc_pd, file_loc_dict, pf_entities, version_mc):
    # causes_mc_result = list()
    # causes_mc_result.append(['cause', '#author', '#cmt', '#changeloc', '#issue', '#issue-cmt', 'issueLoc'])
    # test_entities = list()
    # 求问题实体维护成本
    # TODO：本步骤可在一开始评估时，多加入一列File Path，此处即无需转换
    pf_entities = _format_file_path(all_files_mc_pd['filename'], pf_entities)
    pf_entities_mc = all_files_mc_pd.loc[all_files_mc_pd['filename'].isin(pf_entities)]
    pf_entities_sum_commit = pf_entities_mc['change_loc'].sum()
    pf_entities_sum_loc = pf_entities_mc['change_loc'].sum()
    pf_entities_sum_author = pf_entities_mc['change_loc'].sum()
    # 求出非问题实体的维护成本
    non_pf_entities = all_files_mc_pd['filename'] - pf_entities.keys()
    non_pf_entities_mc = all_files_mc_pd.loc[all_files_mc_pd['filename'].isin(non_pf_entities)]
    non_pf_entities_sum_commit = non_pf_entities_mc['change_loc'].sum()
    non_pf_entities_sum_loc = non_pf_entities_mc['change_loc'].sum()
    non_pf_entities_sum_author = non_pf_entities_mc['change_loc'].sum()
    # 将问题实体和非问题实体的结果写入结果数组
    version_mc.extend(
        [pf_entities_sum_commit, non_pf_entities_sum_commit, pf_entities_sum_commit / non_pf_entities_sum_commit,
         pf_entities_sum_loc, non_pf_entities_sum_loc, pf_entities_sum_loc / non_pf_entities_sum_loc,
         pf_entities_sum_author, non_pf_entities_sum_author, pf_entities_sum_author / non_pf_entities_sum_author])
    # non_pf_entities_cmt = list()
    # non_causes_entities_change_loc = 0
    # non_causes_entities_author = list()
    # non_causes_entities_issue_cmt = list()
    # non_causes_entities_issue_loc = 0
    # non_causes_entities_issue = list()
    # # non_causes_entities = set(list(all_files_mc_dic.keys())) - set(list(new_causes_entities.keys()))
    # non_causes_entity_loc_num = 0
    # for non_causes_entity in non_causes_entities:
    #     if non_causes_entity.replace('\\', '/') in file_loc_dict:
    #         non_causes_entity_loc_num += int(file_loc_dict[non_causes_entity.replace('\\', '/')])
    #         non_causes_entities_cmt.extend(all_files_mc_dic[non_causes_entity]['cmt_id'])
    #         non_causes_entities_change_loc += all_files_mc_dic[non_causes_entity]['change_loc']
    #         non_causes_entities_author.extend(all_files_mc_dic[non_causes_entity]['author_id'])
    #         non_causes_entities_issue_cmt.extend(all_files_mc_dic[non_causes_entity]['issue_cmt_id'])
    #         non_causes_entities_issue_loc += all_files_mc_dic[non_causes_entity]['issue_loc']
    #         non_causes_entities_issue.extend(all_files_mc_dic[non_causes_entity]['issue_id'])
    #
    # causes_entities_cmt = list()
    # causes_entities_change_loc = 0
    # causes_entities_author = list()
    # causes_entities_issue_cmt = list()
    # causes_entities_issue_loc = 0
    # causes_entities_issue = list()
    # causes_entity_loc_num = 0
    # for cause_entity in new_causes_entities:
    #     if cause_entity.replace('\\', '/') in file_loc_dict:
    #         causes_entity_loc_num += int(file_loc_dict[cause_entity.replace('\\', '/')])
    #         causes_entities_cmt.extend(all_files_mc_dic[cause_entity]['cmt_id'])
    #         causes_entities_change_loc += all_files_mc_dic[cause_entity]['change_loc']
    #         causes_entities_author.extend(all_files_mc_dic[cause_entity]['author_id'])
    #         causes_entities_issue_cmt.extend(all_files_mc_dic[cause_entity]['issue_cmt_id'])
    #         causes_entities_issue_loc += all_files_mc_dic[cause_entity]['issue_loc']
    #         causes_entities_issue.extend(all_files_mc_dic[cause_entity]['issue_id'])
    #
    # issue_list.append([len(set(causes_entities_issue)) / causes_entity_loc_num,
    #                    len(set(non_causes_entities_issue)) / non_causes_entity_loc_num])
    # cmt_list.append([len(set(causes_entities_cmt)) / causes_entity_loc_num,
    #                  len(set(non_causes_entities_cmt)) / non_causes_entity_loc_num])
    # change_loc_list.append([causes_entities_change_loc / causes_entity_loc_num,
    #                         non_causes_entities_change_loc / non_causes_entity_loc_num])
    # author_list.append([len(set(causes_entities_author)) / causes_entity_loc_num,
    #                     len(set(non_causes_entities_author)) / non_causes_entity_loc_num])
    # issue_cmt_list.append([len(set(causes_entities_issue_cmt)) / causes_entity_loc_num,
    #                        len(set(non_causes_entities_issue_cmt)) / non_causes_entity_loc_num])
    # issue_loc_list.append([causes_entities_issue_loc / causes_entity_loc_num,
    #                        non_causes_entities_issue_loc / non_causes_entity_loc_num])
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


def _format_file_path(filenames, pf_entities):
    result = dict()
    for pf_entity in pf_entities:
        for file in filenames:
            if pf_entity.replace('.', '\\') in file:
                result[file] = pf_entity
                break
    return result
