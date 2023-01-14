from arch_debt.maintenance_cost_measurement.changeproness import *
from arch_debt.maintenance_cost_measurement.gitlogprocessor import *
from util.csv_operator import write_to_csv, read_csv


def com_mc(project_path, vers, cause_path, out_path):
    causes_entities = read_csv(cause_path, 'causes_entities.csv')
    measure_maintenance(project_path, causes_entities, vers, out_path)


def measure_maintenance(project_path, causes_entities, vers, out_path):
    # coupling_mc_list = list()
    # functionality_mc_list = list()
    author_list = list()
    cmt_list = list()
    change_loc_list = list()
    issue_list = list()
    for version in vers.split('?'):
        os.system('git checkout -f ' + version)
        mc_file = gitlog(project_path, causes_entities, version, author_list, cmt_list, change_loc_list, issue_list)
        out_file = out_path + '/mc/' + version + '/file-mc.csv'
        all_causes_entities_mc_dic = changeProness(causes_entities, mc_file, out_file)
        # compete different causes mc
        causes_mc = com_causes_mc(all_causes_entities_mc_dic)
        write_to_csv(causes_mc, out_path + '/mc/' + version + '/causes-mc.csv')
    return author_list, cmt_list, change_loc_list, issue_list


def com_causes_mc(all_causes_entities_mc_dic):
    causes_mc_result = list()
    causes_mc_result.append(['cause', '#author', '#cmt', '#changeloc', '#issue', '#issue-cmt', 'issueLoc'])
    author = list()
    cmt = list()
    change_loc = 0
    issue = list()
    issue_cmt = list()
    issue_loc = 0
    for entity in all_causes_entities_mc_dic:
        author.extend(all_causes_entities_mc_dic[entity]['author_id'])
        cmt.extend(all_causes_entities_mc_dic[entity]['cmt_id'])
        change_loc += all_causes_entities_mc_dic[entity]['change_loc']
        issue.extend(all_causes_entities_mc_dic[entity]['issue_id'])
        issue_cmt.extend(all_causes_entities_mc_dic[entity]['issue_cmt_id'])
        issue_loc += all_causes_entities_mc_dic[entity]['issue_loc']
        causes_mc_result.append(
                [entity, len(set(author)), len(set(cmt)), change_loc, len(set(issue)), len(set(issue_cmt)), issue_loc])
    # for cause in causes_to_entities:
    #     author = list()
    #     cmt = list()
    #     change_loc = 0
    #     issue = list()
    #     issue_cmt = list()
    #     issue_loc = 0
    #     one_entities_list = list(set(causes_to_entities[cause]))
    #     for entity in one_entities_list:
    #         if entity in all_entities_mc_dic:
    #             author.extend(all_entities_mc_dic[entity]['author_id'])
    #             cmt.extend(all_entities_mc_dic[entity]['cmt_id'])
    #             change_loc += all_entities_mc_dic[entity]['change_loc']
    #             issue.extend(all_entities_mc_dic[entity]['issue_id'])
    #             issue_cmt.extend(all_entities_mc_dic[entity]['issue_cmt_id'])
    #             issue_loc += all_entities_mc_dic[entity]['issue_loc']
    #
    #     causes_mc_result.append(
    #         [cause, len(set(author)), len(set(cmt)), change_loc, len(set(issue)), len(set(issue_cmt)), issue_loc])
    #     if cause == 'coupling':
    #         coupling_mc_list.append(
    #             [len(set(author)), len(set(cmt)), change_loc, len(set(issue)), len(set(issue_cmt)), issue_loc])
    #     else:
    #         functionality_mc_list.append(
    #             [len(set(author)), len(set(cmt)), change_loc, len(set(issue)), len(set(issue_cmt)), issue_loc])
    return causes_mc_result
