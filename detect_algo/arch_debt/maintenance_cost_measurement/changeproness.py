import csv
from util.csv_operator import write_to_csv


def readNodeDict(fileName):
    nodeDict = dict()
    with open(fileName, "r", encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=",")
        for each in reader:
            if each[0] == 'id':
                continue
            id = each[0]
            name = each[1]
            nodeDict[id] = name
    return nodeDict


def read_dep_file(node_file):
    resList = list()
    nodeDict = readNodeDict(node_file)
    # nodeTypeDict = readEdgeDict(edge_file)
    for id in nodeDict.keys():
        name = nodeDict[id]
        tmp = [id, name]
        resList.append(tmp)
    return resList


def formatFileName(file_name_list):
    for index in range(0, len(file_name_list)):
        file_name = file_name_list[index]
        file_name = file_name.replace("/", "\\")
        file_name_list[index] = file_name
    return file_name_list


# read mc file
def read_mc_file(mc_file):
    mc_author_dict = dict()  # [filename][author] = the commit count by this author
    mc_commit_times_dict = dict()  # [filename] = cmttimes
    mc_change_loc_dict = dict()  # [fileName] = loc
    mc_issue_count_dict = dict()  # [fileName][issueId] = issue cmt counts
    mc_issue_loc_dict = dict()  # [fileName][issueId] = issueloc
    with open(mc_file, "r", encoding="utf8") as fp:
        # csv.field_size_limit(500 * 1024 * 1024)
        reader = csv.reader(fp, delimiter=",")
        for each in reader:
            [commit_id, author, date, issue_ids, files, add_locs, del_locs] = each
            file_name_list = files.split(";")
            add_loc_list = add_locs.split(";")
            del_loc_list = del_locs.split(";")
            if issue_ids == "":
                issue_id_list = list()
            else:
                issue_id_list = issue_ids.split(";")

            formatFileName(file_name_list)

            for file_name in file_name_list:
                # author releated
                if file_name not in mc_author_dict:
                    mc_author_dict[file_name] = dict()
                if author not in mc_author_dict[file_name]:
                    mc_author_dict[file_name][author] = 1
                else:
                    mc_author_dict[file_name][author] += 1

            # commit related
            for file_name in file_name_list:
                if file_name not in mc_commit_times_dict:
                    mc_commit_times_dict[file_name] = list()
                mc_commit_times_dict[file_name].append(commit_id)

            # LOC changed related
            for index in range(0, len(file_name_list)):
                file_name = file_name_list[index]
                loc = int(add_loc_list[index]) + int(del_loc_list[index])
                if file_name not in mc_change_loc_dict:
                    mc_change_loc_dict[file_name] = loc
                else:
                    mc_change_loc_dict[file_name] += loc

            # issue counts related
            for index in range(0, len(file_name_list)):
                file_name = file_name_list[index]
                if file_name not in mc_issue_count_dict:
                    mc_issue_count_dict[file_name] = dict()
                for issueId in issue_id_list:
                    if issueId not in mc_issue_count_dict[file_name]:
                        mc_issue_count_dict[file_name][issueId] = list()
                    mc_issue_count_dict[file_name][issueId].append(commit_id)

            # issue loc related
            for index in range(0, len(file_name_list)):
                file_name = file_name_list[index]
                loc = int(add_loc_list[index]) + int(del_loc_list[index])
                if file_name not in mc_issue_loc_dict:
                    mc_issue_loc_dict[file_name] = dict()
                for issueId in issue_id_list:
                    if issueId not in mc_issue_loc_dict[file_name]:
                        mc_issue_loc_dict[file_name][issueId] = loc
                    else:
                        mc_issue_loc_dict[file_name][issueId] += loc
    return mc_author_dict, mc_commit_times_dict, mc_change_loc_dict, mc_issue_count_dict, mc_issue_loc_dict


def search_author_count(mc_author_dict, file_name):
    if file_name in mc_author_dict:
        return len(list(mc_author_dict[file_name].keys())), list(mc_author_dict[file_name].keys())
    else:
        return 0, list()


def search_cmt_count(a_dict, file_name):
    if file_name in a_dict:
        return len(a_dict[file_name]), a_dict[file_name]
    else:
        return 0, list()


def search_count(a_dict, file_name):
    if file_name in a_dict:
        return a_dict[file_name]
    else:
        return 0


def search_issue_count(mc_issue_count_dict, file_name):
    issue_count = 0
    issue_ids = list()
    issue_cmt_count = 0
    issue_cmt_ids = list()
    if file_name in mc_issue_count_dict:
        issue_count = len(list(mc_issue_count_dict[file_name].keys()))
        issue_ids = list(mc_issue_count_dict[file_name].keys())
        for issue_id in mc_issue_count_dict[file_name]:
            issue_cmt_ids.extend(mc_issue_count_dict[file_name][issue_id])
            issue_cmt_count += len(mc_issue_count_dict[file_name][issue_id])

    return issue_count, issue_ids, issue_cmt_count, issue_cmt_ids


def search_issue_loc(mc_issue_loc_dict, file_name):
    if file_name in mc_issue_loc_dict:
        loc = sum(list(mc_issue_loc_dict[file_name].values()))
        return loc
    else:
        return 0


def change_bug_proness_compute(file_list_java, mc_author_dict, mc_commit_times_dict, mc_change_loc_dict,
                               mc_issue_count_dict, mc_issue_loc_dict):
    all_files_mc_list = list()
    all_files_mc_dic = dict()

    for index in range(0, len(file_list_java)):
        file_name = file_list_java[index].replace('/', '\\')
        author_count, authors_id = search_author_count(mc_author_dict, file_name)
        cmt_count, cmt_id = search_cmt_count(mc_commit_times_dict, file_name)
        change_loc = search_count(mc_change_loc_dict, file_name)
        [issue_count, issue_id, issue_cmt_count, issue_cmt_id] = search_issue_count(mc_issue_count_dict, file_name)
        issue_loc = search_issue_loc(mc_issue_loc_dict, file_name)
        # if len(authors_id) != 0 or len(cmt_id) != 0 or change_loc != 0 or len(issue_id) != 0 or len(issue_cmt_id) != 0 or issue_loc != 0:
        all_files_mc_list.append(
            [index, file_name, author_count, cmt_count, change_loc, issue_count, issue_cmt_count, issue_loc])
        all_files_mc_dic[file_name] = {'author_id': authors_id, 'cmt_id': cmt_id,
                                          'change_loc': change_loc, 'issue_id': issue_id,
                                          'issue_cmt_id': issue_cmt_id, 'issue_loc': issue_loc}
    return all_files_mc_list, all_files_mc_dic


def changeProness(file_list_java, mc_file, outfile):
    [mc_author_dict, mc_commit_times_dict, mc_change_loc_dict, mc_issue_count_dict, mc_issue_loc_dict] = read_mc_file(
        mc_file)
    all_files_mc_list, all_files_mc_dic = change_bug_proness_compute(file_list_java, mc_author_dict,
                                                                           mc_commit_times_dict,
                                                                           mc_change_loc_dict, mc_issue_count_dict,
                                                                           mc_issue_loc_dict)
    title = ['id', 'filename', '#author', '#cmt', '#changeloc', '#issue', '#issue-cmt', 'issueLoc']
    final = list()
    final.append(title)
    final.extend(all_files_mc_list)
    write_to_csv(final, outfile)

    return all_files_mc_dic
