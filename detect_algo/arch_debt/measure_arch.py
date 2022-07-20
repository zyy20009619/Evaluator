from detect_algo.arch_debt.maintenance_cost_measurement.changeproness import *
from detect_algo.arch_debt.maintenance_cost_measurement.gitlogprocessor import *
from util.csv_operator import write_to_csv


def measure_maintenance(project_path, causes_entities, causes_to_entities):
    apollo_version_list = 'v0.6.0;v0.6.3;v0.7.0;v0.8.0;v0.9.0;v0.9.1;v0.10.0;v0.10.1;v0.10.2;v0.11.0;v1.0.0;v1.1.0;v1.1.1;v1.1.2;v1.2.0;v1.3.0;v1.4.0;v1.5.0;v1.5.1;v1.6.0;v1.6.1;v1.6.2;v1.7.0;v1.7.1;v1.7.2;v1.8.0;v1.8.1;v1.8.2;v1.9.0;v1.9.1;v1.9.2'.split(
        ';')
    log4_version_list = '2.0.2;2.0.3;2.0.4;2.0.5;2.0.6;2.0.7;2.0.8;2.0.9;2.0.10;2.0.11;2.0.12;2.0.13;2.0.14;2.0.15;2.0.16;2.0.17;2.0.18;2.0.19;2.0.20;2.0.21;2.0.23;2.0.24;2.0.25;2.0.26;2.0.27;2.0.28;2.0.29;2.0.30;2.0.31;2.0.32;2.1.0'.split(
        ';')
    pdfbox_version_list = '1.2.0,1.3.0,1.4.0,1.5.0,1.6.0,1.7.0,1.8.0,1.8.1,1.8.2,1.8.3,1.8.4,1.8.5,1.8.6,1.8.7,1.8.8,1.8.9,1.8.10,1.8.11,1.8.12,1.8.13,1.8.14,1.8.15,1.8.16,2.0.0,2.0.1,2.0.2,2.0.3,2.0.4,2.0.5,2.0.6,2.0.7,2.0.8,2.0.9,2.0.10,2.0.11,2.0.12,2.0.13,2.0.14,2.0.15,2.0.16,2.0.17,2.0.18,2.0.19,2.0.20,2.0.21,2.0.22,2.0.23,2.0.24,2.0.25,2.0.26'.split(
        ',')
    Cassandra_version_list = 'cassandra-1.0.2,cassandra-1.0.3,cassandra-1.0.4,cassandra-1.0.5,cassandra-1.0.6,cassandra-1.0.7,cassandra-1.0.8,cassandra-1.0.9,cassandra-1.0.10,cassandra-1.0.11,cassandra-1.0.12,cassandra-1.1.0,cassandra-1.1.1,cassandra-1.1.2,cassandra-1.1.3,cassandra-1.1.4,cassandra-1.1.5,cassandra-1.1.6,cassandra-1.1.7,cassandra-1.1.8,cassandra-1.1.9,cassandra-1.1.10,cassandra-1.1.11,cassandra-1.1.12,cassandra-1.2.0,cassandra-1.2.1,cassandra-1.2.2,cassandra-1.2.3,cassandra-1.2.4,cassandra-1.2.5,cassandra-1.2.6,cassandra-1.2.7,cassandra-1.2.8,cassandra-1.2.9,cassandra-1.2.10,cassandra-1.2.11,cassandra-1.2.12,cassandra-1.2.13,cassandra-1.2.14,cassandra-1.2.15,cassandra-1.2.16,cassandra-1.2.17,cassandra-1.2.18,cassandra-1.2.19'.split(
        ',')
    CXF_version_list = 'cxf-2.1.3,cxf-2.1.4,cxf-2.1.5,cxf-2.1.6,cxf-2.1.7,cxf-2.1.8,cxf-2.1.9,cxf-2.1.10,cxf-2.2,cxf-2.2.1,cxf-2.2.2,cxf-2.2.3,cxf-2.2.4,cxf-2.2.5,cxf-2.2.6,cxf-2.2.7,cxf-2.2.8,cxf-2.2.9,cxf-2.2.10,cxf-2.2.11,cxf-2.2.12,cxf-2.3.0,cxf-2.3.1,cxf-2.3.2,cxf-2.3.3,cxf-2.3.4,cxf-2.3.5,cxf-2.3.6,cxf-2.3.7,cxf-2.3.8,cxf-2.3.9,cxf-2.3.10,cxf-2.3.11,cxf-2.4.0,cxf-2.4.1,cxf-2.4.2,cxf-2.4.3,cxf-2.4.4,cxf-2.4.5,cxf-2.4.6,cxf-2.4.7,cxf-2.4.8,cxf-2.4.9,cxf-2.4.10'.split(
        ",")
    android_base_version_list = 'android-12.0.0_r3	android-12.0.0_r4	android-12.0.0_r5	android-12.0.0_r6	android-12.0.0_r7	android-12.0.0_r8	android-12.0.0_r9	android-12.0.0_r10	android-12.0.0_r11	android-12.0.0_r12	android-12.0.0_r13	android-12.0.0_r14	android-12.0.0_r15	android-12.0.0_r16	android-12.0.0_r17	android-12.0.0_r18	android-12.0.0_r19	android-12.0.0_r20	android-12.0.0_r21	android-12.0.0_r22'.split(
        "	")
    CalyxOS_base_version_list = 'android-12.0.0_r3	android-12.0.0_r4	android-12.0.0_r5	android-12.0.0_r6	android-12.0.0_r7	android-12.0.0_r8	android-12.0.0_r9	android-12.0.0_r10	android-12.0.0_r11	android-12.0.0_r12'.split("	")

    version_list = list()
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

    index = 1
    for version in apollo_version_list:
        os.system('git checkout ' + version)
        # all commits infos
        mc_file, file_list_java, file_loc_dict = gitlog(project_path, version)
        # all files mc
        out_file = project_path + '/mc/' + version + '/file-mc.csv'
        all_files_mc_dic = changeProness(file_list_java, mc_file, out_file)
        # compete different causes mc
        causes_mc = com_causes_mc(all_files_mc_dic, file_loc_dict, causes_entities, causes_to_entities,
                                  causes_cmt_mc_list, causes_change_loc_mc_list, causes_author_mc_list,
                                  causes_issue_mc_list,
                                  causes_issue_cmt_mc_list, causes_issue_loc_mc_list, cmt_list, change_loc_list,
                                  author_list,
                                  issue_list, issue_cmt_list, issue_loc_list)
        write_to_csv(causes_mc, project_path + '/mc/' + version + '/causes-mc.csv')
        version_list.append(index)
        index += 1
    return [version_list, causes_cmt_mc_list, causes_change_loc_mc_list, causes_author_mc_list, causes_issue_mc_list,
            causes_issue_cmt_mc_list, causes_issue_loc_mc_list, cmt_list, change_loc_list, author_list, issue_list,
            issue_cmt_list, issue_loc_list, all_files_mc_dic]


def _format_file_path(all_files_mc_dic, causes_entities):
    result = dict()
    for causes_entity in list(set(causes_entities)):
        for file in all_files_mc_dic:
            if causes_entity.replace('.', '\\') in file:
                result[file] = causes_entity
                break
    return result


def com_causes_mc(all_files_mc_dic, file_loc_dict, causes_entities, causes_to_entities, causes_cmt_mc_list,
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

    issue_list.append([len(list(set(causes_entities_issue))) / causes_entity_loc_num,
                       len(list(set(non_causes_entities_issue))) / non_causes_entity_loc_num])
    cmt_list.append([len(list(set(causes_entities_cmt))) / causes_entity_loc_num,
                     len(list(set(non_causes_entities_cmt))) / non_causes_entity_loc_num])
    change_loc_list.append([causes_entities_change_loc / causes_entity_loc_num,
                            non_causes_entities_change_loc / non_causes_entity_loc_num])
    author_list.append([len(list(set(causes_entities_author))) / causes_entity_loc_num,
                        len(list(set(non_causes_entities_author))) / non_causes_entity_loc_num])
    issue_cmt_list.append([len(list(set(causes_entities_issue_cmt))) / causes_entity_loc_num,
                           len(list(set(non_causes_entities_issue_cmt))) / non_causes_entity_loc_num])
    issue_loc_list.append([causes_entities_issue_loc / causes_entity_loc_num,
                           non_causes_entities_issue_loc / non_causes_entity_loc_num])

    for cause in causes_to_entities:
        author = list()
        cmt = list()
        change_loc = 0
        issue = list()
        issue_cmt = list()
        issue_loc = 0
        one_entities_list = list(set(causes_to_entities[cause]))
        loc_num = 0
        for entity in one_entities_list:
            for file in all_files_mc_dic:
                if entity.replace('.', '\\') in file:
                    loc_num += int(file_loc_dict[file.replace('\\', '/')])
                    author.extend(all_files_mc_dic[file]['author_id'])
                    cmt.extend(all_files_mc_dic[file]['cmt_id'])
                    change_loc += all_files_mc_dic[file]['change_loc']
                    issue.extend(all_files_mc_dic[file]['issue_id'])
                    issue_cmt.extend(all_files_mc_dic[file]['issue_cmt_id'])
                    issue_loc += all_files_mc_dic[file]['issue_loc']
                    break
        if cause == 'inherit':
            inherit_cmt_mc = len(set(cmt)) / loc_num
            inherit_change_loc_mc = change_loc / loc_num
            inherit_author_mc = len(set(author)) / loc_num
            inherit_issue_mc = len(set(issue)) / loc_num
            inherit_issue_cmt_mc = len(set(issue_cmt)) / loc_num
            inherit_issue_loc_mc = issue_loc / loc_num
        if cause == 'call':
            call_cmt_mc = len(set(cmt)) / loc_num
            call_change_loc_mc = change_loc / loc_num
            call_author_mc = len(set(author)) / loc_num
            call_issue_mc = len(set(issue)) / loc_num
            call_issue_cmt_mc = len(set(issue_cmt)) / loc_num
            call_issue_loc_mc = issue_loc / loc_num
        if cause == 'import':
            import_cmt_mc = len(set(cmt)) / loc_num
            import_change_loc_mc = change_loc / loc_num
            import_author_mc = len(set(author)) / loc_num
            import_issue_mc = len(set(issue)) / loc_num
            import_issue_cmt_mc = len(set(issue_cmt)) / loc_num
            import_issue_loc_mc = issue_loc / loc_num
        if cause == 'functionality':
            functionality_cmt_mc = len(set(cmt)) / loc_num
            functionality_change_loc_mc = change_loc / loc_num
            functionality_author_mc = len(set(author)) / loc_num
            functionality_issue_mc = len(set(issue)) / loc_num
            functionality_issue_cmt_mc = len(set(issue_cmt)) / loc_num
            functionality_issue_loc_mc = issue_loc / loc_num

        causes_mc_result.append(
            [cause, len(set(author)), len(set(cmt)), change_loc, len(set(issue)), len(set(issue_cmt)), issue_loc])
    causes_cmt_mc_list.append([inherit_cmt_mc, call_cmt_mc, import_cmt_mc, functionality_cmt_mc])
    causes_change_loc_mc_list.append(
        [inherit_change_loc_mc, call_change_loc_mc, import_change_loc_mc, functionality_change_loc_mc])
    causes_author_mc_list.append(
        [inherit_author_mc, call_author_mc, import_author_mc, functionality_author_mc])
    causes_issue_mc_list.append(
        [inherit_issue_mc, call_issue_mc, import_issue_mc, functionality_issue_mc])
    causes_issue_cmt_mc_list.append(
        [inherit_issue_cmt_mc, call_issue_cmt_mc, import_issue_cmt_mc, functionality_issue_cmt_mc])
    causes_issue_loc_mc_list.append(
        [inherit_issue_loc_mc, call_issue_loc_mc, import_issue_loc_mc, functionality_issue_loc_mc])
    return causes_mc_result
