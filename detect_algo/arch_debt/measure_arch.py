from detect_algo.arch_debt.maintenance_cost_measurement.changeproness import *
from detect_algo.arch_debt.maintenance_cost_measurement.gitlogprocessor import *
from util.csv_operator import write_to_csv


def measure_maintenance(project_path, causes_entities, causes_to_entities):
    # apollo_version_list = 'v0.6.0;v0.6.3;v0.7.0;v0.8.0;v0.9.0;v0.9.1;v0.10.0;v0.10.1;v0.10.2;v0.11.0;v1.0.0;v1.1.0;v1.1.1;v1.1.2;v1.2.0;v1.3.0;v1.4.0;v1.5.0;v1.5.1;v1.6.0;v1.6.1;v1.6.2;v1.7.0;v1.7.1;v1.7.2;v1.8.0;v1.8.1;v1.8.2;'.split(
    #     ';')
    log4_version_list = '2.0.2;2.0.3;2.0.4;2.0.5;2.0.6;2.0.7;2.0.8;2.0.9;2.0.10;2.0.11;2.0.12;2.0.13;2.0.14;2.0.15;2.0.16;2.0.17;2.0.18;2.0.19;2.0.20;2.0.21;2.0.23;2.0.24;2.0.25;2.0.26;2.0.27;2.0.28;2.0.29;2.0.30;2.0.31;2.0.32;'.split(
        ';')
    version_list = list()
    coupling_mc_list = list()
    functionality_mc_list = list()
    author_list = list()
    cmt_list = list()
    change_loc_list = list()
    issue_list = list()
    index = 1
    for version in log4_version_list:
        os.system('git checkout ' + version)
        mc_file = gitlog(project_path, causes_entities, version, author_list, cmt_list, change_loc_list, issue_list)
        out_file = project_path + '/mc/' + version + '/file-mc.csv'
        all_entities_mc_dic = changeProness(causes_entities, mc_file, out_file)
        # compete different causes mc
        causes_mc = com_causes_mc(all_entities_mc_dic, causes_to_entities, coupling_mc_list, functionality_mc_list)
        write_to_csv(causes_mc, project_path + '/mc/' + version + '/causes-mc.csv')
        version_list.append(index)
        index += 1
    return version_list, coupling_mc_list, functionality_mc_list, author_list, cmt_list, change_loc_list, issue_list


def com_causes_mc(all_entities_mc_dic, causes_to_entities, coupling_mc_list, functionality_mc_list):
    causes_mc_result = list()
    causes_mc_result.append(['cause', '#author', '#cmt', '#changeloc', '#issue', '#issue-cmt', 'issueLoc'])
    for cause in causes_to_entities:
        author = list()
        cmt = list()
        change_loc = 0
        issue = list()
        issue_cmt = list()
        issue_loc = 0
        one_entities_list = list(set(causes_to_entities[cause]))
        for entity in one_entities_list:
            if entity in all_entities_mc_dic:
                author.extend(all_entities_mc_dic[entity]['author_id'])
                cmt.extend(all_entities_mc_dic[entity]['cmt_id'])
                change_loc += all_entities_mc_dic[entity]['change_loc']
                issue.extend(all_entities_mc_dic[entity]['issue_id'])
                issue_cmt.extend(all_entities_mc_dic[entity]['issue_cmt_id'])
                issue_loc += all_entities_mc_dic[entity]['issue_loc']

        causes_mc_result.append(
            [cause, len(set(author)), len(set(cmt)), change_loc, len(set(issue)), len(set(issue_cmt)), issue_loc])
        if cause == 'coupling':
            coupling_mc_list.append(
                [len(set(author)), len(set(cmt)), change_loc, len(set(issue)), len(set(issue_cmt)), issue_loc])
        else:
            functionality_mc_list.append(
                [len(set(author)), len(set(cmt)), change_loc, len(set(issue)), len(set(issue_cmt)), issue_loc])
    return causes_mc_result
