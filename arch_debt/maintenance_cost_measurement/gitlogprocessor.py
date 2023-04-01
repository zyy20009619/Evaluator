import re
import os
from util.csv_operator import write_to_csv
from arch_debt.maintenance_cost_measurement.basedata import *
from util.path_operator import create_file_path


def generateLog(project_path, out_path):
    # os.system('git checkout -f ' + version)
    # os.chdir(project_path)

    git_log_file = create_file_path(out_path, 'gitlog')
    git_loc_file = create_file_path(out_path, 'gitloc')
    # 获取git log文件
    os.system('git log --numstat --date=iso > ' + git_log_file)
    # 获取git loc文件
    # os.system('git ls-files | xargs wc -l > ' + git_loc_file)

    return git_log_file, git_loc_file


def processGitLog(file_name, file_list_java):
    commit_collection_java = list()

    commit_id = ""
    author_name = ""
    date = ""
    file_list = list()
    add_list = list()
    del_list = list()
    issue_ids = list()

    fp = open(file_name, encoding="utf8", errors='ignore')
    num = 0
    for line in fp:
        num += 1
        if re.match("commit\s[0-9a-zA-Z]+", line):
            if commit_id != "":
                [is_kept, one_commit] = processPreCmt(commit_id, author_name, date, file_list, add_list, del_list,
                                                      issue_ids, file_list_java)
                if is_kept:
                    commit_collection_java.append(one_commit)
                file_list = list()
                del_list = list()
                add_list = list()
                issue_ids = list()

            match = re.match("commit\s[0-9a-zA-Z]+", line)
            commit_id = match.group().split("commit ")[1]
        elif re.match("Author: ", line):
            str_list = line.split("Author: ")[1].split("<")
            author_name = str_list[0].strip()
        elif re.match("Date:   ", line):
            date = line.split("Date:   ")[1].strip("\n")
        elif re.match("[0-9]+	[0-9]+	", line):
            str_list = line.strip("\n").split("	")
            add_loc = int(str_list[0])
            del_loc = int(str_list[1])
            file_name = str_list[2]
            file_list.append(file_name)
            add_list.append(add_loc)
            del_list.append(del_loc)
        elif re.findall("#[0-9]+", line):
            match = re.findall("#[0-9]+", line)
            for issueId in match:
                issue_ids.append(int(issueId.split("#")[1]))
    [is_kept, one_commit] = processPreCmt(commit_id, author_name, date, file_list, add_list, del_list, issue_ids,
                                          file_list_java)
    if is_kept:
        commit_collection_java.append(one_commit)
    fp.close()
    return commit_collection_java


def processPreCmt(commit_id, author_name, date, file_list, add_list, del_list, issue_ids, file_list_java):
    new_file_list = list()
    new_del_list = list()
    new_add_list = list()
    for index in range(0, len(file_list)):
        if file_list[index] in file_list_java:
            new_file_list.append(file_list[index])
            new_del_list.append(del_list[index])
            new_add_list.append(add_list[index])

    if len(new_file_list) == 0:
        is_kept = False
    else:
        is_kept = True
    modify_detail = ModifyDetail(new_file_list, new_add_list, new_del_list)
    one_commit = CommitDetail(commit_id, author_name, date, issue_ids, modify_detail)
    return is_kept, one_commit


def getAllFilesByFilter(project_path):
    file_list_all = list()
    file_list_java = list()
    file_list_notest = list()

    for filename, dirs, files in os.walk(project_path, topdown=True):
        filename = filename.split(project_path)[1]
        filename = filename.replace("\\", "/")
        if filename.startswith(".git") or filename.startswith(".github"):
            continue
        for file in files:
            file_temp = filename + "\\" + file
            file_temp = file_temp[1:]
            file_temp = file_temp.replace("\\", "/")
            file_list_all.append(file_temp)
            if file.endswith(".java"):
                file_list_java.append(file_temp)
                if "tests\\" not in file and "test\\" not in file:
                    file_list_notest.append(file_temp)
    return file_list_all, file_list_java, file_list_notest


def saveCommitCollection(commit_collection):
    res_list = list()
    for one_commit in commit_collection:
        row = one_commit.toList()
        res_list.append(row)
    return res_list


def gitlog(project_path, version, base_version_path):
    git_log_file, git_loc_file = generateLog(version, base_version_path)
    file_list_java = get_all_files_by_filter(project_path)
    # 统计所有java文件的loc
    file_loc_dict = git_loc(git_loc_file, file_list_java)
    # 统计所有java文件的commit信息
    commit_collection_java = processGitLog(git_log_file, file_list_java)
    commit_collection_res = saveCommitCollection(commit_collection_java)
    # write_to_csv(commit_collection_res_list, create_file_path(base_version_path, 'history-java.csv'))

    return commit_collection_res, file_list_java, file_loc_dict


def git_loc(git_loc_file, file_list_java):
    file_loc_dic = dict()
    # os.chdir(project_path)

    # del gitloc file
    fp = open(git_loc_file, encoding="utf8", errors='ignore')
    for line in fp:
        split_rs = line.split(' ')
        loc = split_rs[len(split_rs) - 2]
        file_name = split_rs[len(split_rs) - 1].replace('\n', '')
        if file_name in file_list_java:
            file_loc_dic[file_name] = loc
    return file_loc_dic


def get_all_files_by_filter(project_path):
    file_list_java = list()
    for filename, dirs, files in os.walk(project_path, topdown=True):
        filename = filename.split(project_path)[1]
        filename = filename.replace("\\", "/")
        if filename.startswith(".git") or filename.startswith(".github"):
            continue
        for file in files:
            file_temp = filename + "\\" + file
            file_temp = file_temp[1:]
            file_temp = file_temp.replace("\\", "/")
            if file.endswith(".java"):
                file_list_java.append(file_temp)
    return file_list_java


def get_file_mc(project_path, out_path, project_name):
    gitlogFile = generateLog(project_path, out_path)
    [fileList_all, fileList_java, fileList_notest] = getAllFilesByFilter(project_path)

    commitCollection_java = processGitLog(gitlogFile, fileList_java)

    resList = saveCommitCollection(commitCollection_java)
    write_to_csv(resList, os.path.join(out_path, 'history-java.csv'))

    return os.path.join(out_path, 'history-java.csv')