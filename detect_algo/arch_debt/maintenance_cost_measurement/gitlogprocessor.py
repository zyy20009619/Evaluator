import re
import subprocess
import os
from pathlib import Path
from util.csv_operator import write_to_csv
from detect_algo.arch_debt.maintenance_cost_measurement.basedata import *


def generateLog(project_path, version):
    mc_dir = project_path + "//mc//" + version

    if not os.path.exists(mc_dir):
        os.makedirs(mc_dir)
    os.chdir(project_path)

    git_log_file = mc_dir + "//gitlog"
    # --numstat:count the number of code churn(add and delete)
    cmd = "git log --numstat --date=iso > " + git_log_file
    subprocess.call(cmd, shell=True)

    return git_log_file


def processGitLog(file_name, causes_entities, author_list, cmt_list, change_loc_list, issue_list):
    commit_collection_causes_entities = list()

    commit_id = ""
    author_name = ""
    date = ""
    file_list = list()
    add_list = list()
    del_list = list()
    issue_ids = list()
    temp_author_list = list()
    temp_cmt_list = list()
    temp_change_loc = 0
    temp_issue_list = list()

    fp = open(file_name, encoding="utf8", errors='ignore')
    num = 0
    for line in fp:
        num += 1
        if re.match("commit\s[0-9a-zA-Z]+", line):
            if commit_id != "":
                [is_kept, one_commit] = processPreCmt(commit_id, author_name, date, file_list, add_list, del_list,
                                                      issue_ids, causes_entities)
                if is_kept:
                    commit_collection_causes_entities.append(one_commit)
                file_list = list()
                del_list = list()
                add_list = list()
                issue_ids = list()

            match = re.match("commit\s[0-9a-zA-Z]+", line)
            commit_id = match.group().split("commit ")[1]
            temp_cmt_list.append(commit_id)
        elif re.match("Author: ", line):
            str_list = line.split("Author: ")[1].split("<")
            author_name = str_list[0].strip()
            temp_author_list.append(author_name)
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
            temp_change_loc += add_loc
            temp_change_loc += del_loc
        elif re.findall("#[0-9]+", line):
            match = re.findall("#[0-9]+", line)
            for issueId in match:
                issue_ids.append(int(issueId.split("#")[1]))
            temp_issue_list.extend(issue_ids)
    [is_kept, one_commit] = processPreCmt(commit_id, author_name, date, file_list, add_list, del_list, issue_ids,
                                          causes_entities)
    if is_kept:
        commit_collection_causes_entities.append(one_commit)
    fp.close()
    author_list.append(list(set(temp_author_list)))
    cmt_list.append(list(set(temp_cmt_list)))
    change_loc_list.append(temp_change_loc)
    issue_list.append(list(set(temp_issue_list)))
    return commit_collection_causes_entities


def processPreCmt(commit_id, author_name, date, file_list, add_list, del_list, issue_ids, causes_entities):
    new_file_list = list()
    new_del_list = list()
    new_add_list = list()
    for index in range(0, len(file_list)):
        for causes_entity in causes_entities:
            if causes_entity.replace('.', '/') in file_list[index]:
                new_file_list.append(causes_entity)
                new_del_list.append(del_list[index])
                new_add_list.append(add_list[index])
                break

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


def gitlog(project_path, causes_entities, version, author_list, cmt_list, change_loc_list, issue_list):
    git_log_file = generateLog(project_path, version)
    commit_collection_causes_entities = processGitLog(git_log_file, causes_entities, author_list, cmt_list,
                                                      change_loc_list, issue_list)

    res_list = saveCommitCollection(commit_collection_causes_entities)
    mc_file = project_path + '//mc//' + version + '//causes_entities.csv'
    write_to_csv(res_list, mc_file)

    return mc_file
