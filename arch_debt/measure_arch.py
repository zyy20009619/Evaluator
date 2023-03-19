import os

import pandas as pd

from arch_debt.maintenance_cost_measurement.changeproness import *
from arch_debt.maintenance_cost_measurement.gitlogprocessor import *
from util.csv_operator import write_to_csv, read_csv, read_csv_to_pd
from util.path_operator import create_dir_path


def com_mc(project_path, vers, detect_path, pro_name, method):
    # causes_entities = read_csv(cause_path, 'causes_entities.csv')
    if method == 'ours':
        detection_res = read_csv_to_pd(os.path.join(detect_path, 'detection result.csv'))
        measure_maintenance(project_path,
                            list(set(detection_res[detection_res['class status'] != 'delete']['problem class'])), vers,
                            detect_path, pro_name)
    elif method == 'dv8':
        extract_dv8_pf_files(project_path, vers, pro_name, method)


def extract_dv8_pf_files(project_path, vers, pro_name, method):
    compare_base_path = r'D:\paper-data-and-result\results\bishe-results\compare-result\dv8'
    file_path = compare_base_path + '/' + pro_name + '/dv8-analysis-result/file-measure-report.csv'
    dv8_pd = read_csv_to_pd(file_path)
    pf_pd = dv8_pd[
        ['FileName', 'numCrossing', 'numModularityViolation', 'numPackageCycle', 'numUnhealthyInheritance',
         'numUnstableInterface', 'numClique']]
    # pf_pd.replace('/', '\\', inplace=True)
    crossing_files = pf_pd[pf_pd['numCrossing'] != 0]['FileName']
    modularity_violation_files = pf_pd[pf_pd['numModularityViolation'] != 0]['FileName']
    package_cycle_files = pf_pd[pf_pd['numPackageCycle'] != 0]['FileName']
    unhealthy_inheritance_files = pf_pd[pf_pd['numUnhealthyInheritance'] != 0]['FileName']
    unstable_interface_files = pf_pd[pf_pd['numUnstableInterface'] != 0]['FileName']
    clique_files = pf_pd[pf_pd['numClique'] != 0]['FileName']

    all_pf_files = pd.concat(
        [crossing_files, modularity_violation_files, package_cycle_files, unhealthy_inheritance_files,
         unstable_interface_files, clique_files], axis=0).reset_index(drop=True)

    # 计算维护成本
    measure_maintenance(project_path, crossing_files, vers,
                        create_dir_path(os.path.join(r'D:\paper-data-and-result\results\bishe-results\compare-result\dv8',
                                     pro_name + '\crossing')), pro_name, method)
    measure_maintenance(project_path, modularity_violation_files, vers,
                        create_dir_path(os.path.join(r'D:\paper-data-and-result\results\bishe-results\compare-result\dv8',
                                     pro_name + '\cmodularity_violation')), pro_name, method)
    measure_maintenance(project_path, package_cycle_files, vers,
                        create_dir_path(os.path.join(r'D:\paper-data-and-result\results\bishe-results\compare-result\dv8',
                                     pro_name + '\package_cycle')), pro_name, method)
    measure_maintenance(project_path, unhealthy_inheritance_files, vers,
                        create_dir_path(os.path.join(r'D:\paper-data-and-result\results\bishe-results\compare-result\dv8',
                                     pro_name + '\\unhealthy_inheritance')), pro_name, method)
    measure_maintenance(project_path, unstable_interface_files, vers,
                        create_dir_path(os.path.join(r'D:\paper-data-and-result\results\bishe-results\compare-result\dv8',
                                     pro_name + '\\unstable_interface')), pro_name, method)
    measure_maintenance(project_path, clique_files, vers,
                        create_dir_path(os.path.join(r'D:\paper-data-and-result\results\bishe-results\compare-result\dv8',
                                     pro_name + '\clique')), pro_name, method)
    measure_maintenance(project_path, all_pf_files, vers,
                        create_dir_path(os.path.join(r'D:\paper-data-and-result\results\bishe-results\compare-result\dv8',
                                     pro_name + '\\all_pf')), pro_name, method)


def measure_maintenance(project_path, pf_entities, vers, output_path, pro_name, method):
    if pf_entities.empty:
        return
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
        version = version.replace('\n', '')
        version_mc = list()
        version_mc.append(version)
        base_version_path = os.path.join(os.path.join(r'D:\paper-data-and-result\results\paper-results\mv',
                                                      pro_name + '-enre-out'),
                                         'mc/' + version)
        # 获取到该版本的loc和log，计算版本中每个文件的维护成本
        commit_collection_res, file_list_java, file_loc_dict = gitlog(project_path, version, base_version_path)
        # 计算所有文件的维护成本
        all_files_mc_pd = changeProness(file_list_java, commit_collection_res,
                                        create_file_path(base_version_path, 'file mc.csv'))
        # 计算问题实体和非问题实体的维护成本
        com_pfs_mc(all_files_mc_pd, file_loc_dict, pf_entities, version_mc, method)
        mc_list.append(version_mc)
    res_pf = pd.DataFrame(data=mc_list, columns=['version', '#commit-mc(A)', '#commit-mc(B)', '#commit-average(P)',
                                                 '#changeLoc-mc(A)', '#changeLoc-mc(B)', '#changeLoc-average(P)',
                                                 '#author-mc(A)', '#author-mc(B)', '#author-average(P)'])
    res_pf['projectname'] = os.path.basename(project_path)
    res_pf.to_csv(os.path.join(output_path, "mc result.csv"), index=False, sep=',')
    # write_to_csv(cmt_list, out_path + '/mc/causes_cmt.csv')
    # write_to_csv(change_loc_list, out_path + '/mc/causes_change_loc.csv')
    # write_to_csv(author_list, out_path + '/mc/causes_author.csv')
    # 切换回当前工作目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # write_to_csv(issue_list, out_path + '/mc/causes_issue.csv')
    # write_to_csv(issue_cmt_list, out_path + '/mc/causes_issue_cmt.csv')
    # write_to_csv(issue_loc_list, out_path + '/mc/causes_issue_loc.csv')


def com_pfs_mc(all_files_mc_pd, file_loc_dict, pf_entities, version_mc, method):
    # causes_mc_result = list()
    # causes_mc_result.append(['cause', '#author', '#cmt', '#changeloc', '#issue', '#issue-cmt', 'issueLoc'])
    # test_entities = list()
    # TODO：本步骤可在一开始评估时，多加入一列File Path，此处即无需转换
    # TODO:此处先使用之前的代码逻辑计算维护成本，实验全部做完之后再优化代码
    # 求问题实体维护成本
    pf_entities = _format_file_path(all_files_mc_pd['filename'], pf_entities, method)
    pf_entities_cmt = list()
    pf_entities_change_loc = 0
    pf_entities_author = list()
    # causes_entities_issue_cmt = list()
    # causes_entities_issue_loc = 0
    # causes_entities_issue = list()
    pf_entity_loc_num = 0
    for pf_entity in pf_entities:
        if pf_entity.replace('\\', '/') in file_loc_dict:
            pf_entity_loc_num += int(file_loc_dict[pf_entity.replace('\\', '/')])
            pf_entities_cmt.extend(list(all_files_mc_pd[all_files_mc_pd['filename'] == pf_entity]['cmt_id'])[0])
            pf_entities_change_loc += list(all_files_mc_pd[all_files_mc_pd['filename'] == pf_entity]['change_loc'])[0]
            pf_entities_author.extend(list(all_files_mc_pd[all_files_mc_pd['filename'] == pf_entity]['author_id'])[0])
            # causes_entities_issue_cmt.extend(
            #     all_files_mc_pd[all_files_mc_pd['filename'] == cause_entity]['issue_cmt_id'])
            # causes_entities_issue_loc += all_files_mc_pd[all_files_mc_pd['filename'] == cause_entity]['issue_loc']
            # causes_entities_issue.extend(all_files_mc_pd[all_files_mc_pd['filename'] == cause_entity]['issue_id'])

    # pf_entities_mc = all_files_mc_pd.loc[all_files_mc_pd['filename'].isin(pf_entities)]
    # pf_entities_sum_commit = pf_entities_mc['change_loc'].sum()
    # pf_entities_sum_loc = pf_entities_mc['change_loc'].sum()
    # pf_entities_sum_author = pf_entities_mc['change_loc'].sum()
    # 求出非问题实体的维护成本(差集)
    non_pf_entities = all_files_mc_pd[~(all_files_mc_pd['filename'].isin(pf_entities.keys()))]['filename']
    non_pf_entities_cmt = list()
    non_pf_entities_change_loc = 0
    non_pf_entities_author = list()
    # non_causes_entities_issue_cmt = list()
    # non_causes_entities_issue_loc = 0
    # non_causes_entities_issue = list()
    # non_causes_entities = set(list(all_files_mc_dic.keys())) - set(list(new_causes_entities.keys()))
    non_pf_entity_loc_num = 0
    for non_pf_entity in non_pf_entities:
        if non_pf_entity.replace('\\', '/') in file_loc_dict:
            non_pf_entity_loc_num += int(file_loc_dict[non_pf_entity.replace('\\', '/')])
            non_pf_entities_cmt.extend(list(all_files_mc_pd[all_files_mc_pd['filename'] == non_pf_entity]['cmt_id'])[0])
            non_pf_entities_change_loc += \
                list(all_files_mc_pd[all_files_mc_pd['filename'] == non_pf_entity]['change_loc'])[0]
            non_pf_entities_author.extend(
                list(all_files_mc_pd[all_files_mc_pd['filename'] == non_pf_entity]['author_id'])[0])
            # non_causes_entities_issue_cmt.extend(all_files_mc_pd[all_files_mc_pd['filename'] == non_pf_entity]]['issue_cmt_id'])
            # non_causes_entities_issue_loc += all_files_mc_pd[all_files_mc_pd['filename'] == non_pf_entity]]['issue_loc']
            # non_causes_entities_issue.extend(all_files_mc_pd[all_files_mc_pd['filename'] == non_pf_entity]]['issue_id'])

    # non_pf_entities_mc = all_files_mc_pd.loc[all_files_mc_pd['filename'].isin(non_pf_entities)]
    # non_pf_entities_sum_commit = non_pf_entities_mc['change_loc'].sum()
    # non_pf_entities_sum_loc = non_pf_entities_mc['change_loc'].sum()
    # non_pf_entities_sum_author = non_pf_entities_mc['change_loc'].sum()
    # 将问题实体和非问题实体的结果写入结果数组
    version_mc.extend(
        [len(set(pf_entities_cmt)) / pf_entity_loc_num, len(set(non_pf_entities_cmt)) / non_pf_entity_loc_num,
         (len(set(pf_entities_cmt)) / pf_entity_loc_num) / (len(set(non_pf_entities_cmt)) / non_pf_entity_loc_num),
         pf_entities_change_loc / pf_entity_loc_num, non_pf_entities_change_loc / non_pf_entity_loc_num,
         (pf_entities_change_loc / pf_entity_loc_num) / (non_pf_entities_change_loc / non_pf_entity_loc_num),
         len(set(pf_entities_author)) / pf_entity_loc_num, len(set(non_pf_entities_author)) / non_pf_entity_loc_num,
         (len(set(pf_entities_author)) / pf_entity_loc_num) / (
                 len(set(non_pf_entities_author)) / non_pf_entity_loc_num)])

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


def _format_file_path(filenames, pf_entities, method):
    result = dict()
    for pf_entity in pf_entities:
        for file in filenames:
            if (method == 'ours' and pf_entity.replace('.', '\\') in file) or (method == 'dv8' and pf_entity.replace('/', '\\') in file):
                result[file] = pf_entity
                break
    return result
