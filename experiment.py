# coding=utf-8
import os
import shutil
import csv
import subprocess
import pandas as pd
import numpy as np
from function_file import measure_package_metrics, compare_diff
from detect_algo.detect_root_cause import analyse_data
from arch_debt.measure_arch import com_mc
from arch_debt.compute_bench_mc_metric import com_gt
from util.metrics import PROJECT_METRICS
from util.csv_operator import read_csv_to_pd
from arch_debt.measure_arch import com_mc
from util.json_operator import read_file
from util.path_operator import create_dir_path
from score_compete.index_measure import get_score
from scipy.stats import pearsonr


# 克隆代码并且计算每个项目的SCORE
def clone_code():
    base_path = r'D:\paper-data-and-result\results\bishe-results\subjects.csv'
    pro_out_path = r'D:\paper-data-and-result\results\bishe-results\metrics-rsult\projects'
    SCORE_out_path = r'D:\paper-data-and-result\results\bishe-results\metrics-rsult\SCORE\component\all'
    measure_out_path = r'D:\paper-data-and-result\results\bishe-results\metrics-rsult\measure_results\component'
    gt_out_path = r'D:\paper-data-and-result\results\bishe-results\metrics-rsult\gt'
    subjects_pd = read_csv_to_pd(base_path)
    subjects_pd = subjects_pd[['project name ', 'version']]

    # os.chdir(pro_out_path)
    score = list()
    gt_list = list()
    for index, row in subjects_pd.iterrows():
        print(row[0])
        vers = row[1].split('?')
        # os.system('git clone ' + row[1])
        for ver in vers:
            # 调用指标计算方法计算指标结果(粒度：package/component)
            measure_package_metrics(os.path.join(pro_out_path, row[0]), '',
                                    os.path.join(measure_out_path, row[0]), ver,
                                    'java', 'component')
            # 根据需求计算SCORE值
            # metrics = ['module_name','scoh', 'scop', 'odd', 'idd']
            # weight = [[0.25], [0.25], [0.25], [0.25]]
            # metrics = ['module_name', 'scoh', 'scop', 'odd', 'idd', 'spread', 'focus', 'icf', 'ecf', 'rei', 'chm',
            #            'chd',
            #            'DSM']
            # weight = [[0.1], [0.1], [0.08], [0.08], [0.08], [0.08], [0.08], [0.08], [0.08], [0.08], [0.08], [0.08]]
            # # metrics = ['module_name', 'scoh', 'scop', 'odd', 'idd', 'spread', 'focus', 'icf', 'ecf', 'rei']
            # # weight = [[0.1], [0.1], [0.1], [0.1], [0.12], [0.12], [0.12], [0.12], [0.12]]
            # measure_path = os.path.join(measure_out_path, row[0])
            # if os.path.exists(measure_path):
            #     measure_pd = read_csv_to_pd(measure_path + '\\measure_result_class.csv')
            #     module_list = measure_pd[metrics]
            #     module_list.drop_duplicates(subset=['module_name'], keep='first', inplace=True)
            #     del module_list['module_name']
            #     [normalized_result, score_result] = get_score(module_list.values, weight, metrics[1:])
            # score.append([row[0], ver, np.mean(score_result)])
            # # 计算groundtruth指标
            # com_gt(os.path.join(pro_out_path, row[0]), os.path.join(gt_out_path, row[0]), ver, gt_list)
    # gt_pd = pd.DataFrame(data=gt_list, columns=['project', 'CCOR', 'BCOR', 'CCFOR', 'BCFOR', 'CPCO', 'BPCO'])
    # gt_pd.to_csv(os.path.join(gt_out_path, "gt.csv"), index=False, sep=',')
    # score_pd = pd.DataFrame(data=score, columns=['project', 'version', 'score'])
    # gt_pd = pd.DataFrame(data=gt_list, columns=['version', 'CCOR', 'BCOR', 'CCFOR', 'BCFOR', 'CPCO', 'BPCO'])
    # compare_pd = pd.merge(score_pd, gt_pd, how='inner', on='version')
    # # 计算本方法结果和gt结果相关性
    # print('CCOR:')
    # r1 = pearsonr(compare_pd['score'], compare_pd['CCOR'])
    # print("pearson系数：", r1[0])
    # print("   P-Value：", r1[1])
    # print('CCFOR:')
    # r2 = pearsonr(compare_pd['score'], compare_pd['CCFOR'])
    # print("pearson系数：", r2[0])
    # print("P-Value：", r2[1])
    # print('CPCO:')
    # r3 = pearsonr(compare_pd['score'], compare_pd['CPCO'])
    # print("pearson系数：", r3[0])
    # print("   P-Value：", r3[1])
    # compare_pd.to_csv(os.path.join(SCORE_out_path, "score.csv"), index=False, sep=',')


# 编译java文件
def out_file_list(pro_name, pro_path, version):
    base_out_path = r'D:\paper-data-and-result\results\bishe-results\mc-result\dbMIT-results' + '\\' + pro_name + '\\' + \
                    version[0]
    arcade_out_path = create_dir_path(
        r'D:\paper-data-and-result\results\bishe-results\mc-result\ARCADE-results' + '\\' + pro_name + '\\' + 'classfiles')

    dep_dic = read_file(os.path.join(base_out_path, pro_name + '-out.json'))
    variables = dep_dic['variables']
    # path_to_qualifiedName = list()
    os.chdir(pro_path)
    os.system("git checkout -f " + version[0])
    for var in variables:
        if var['category'] == 'File':
            # path_to_qualifiedName.append(var['File'])
            os.system('javac ' + var['File'] + ' -d ' + arcade_out_path + ' -encoding utf-8')
    # file_pd = pd.DataFrame(data=path_to_qualifiedName)


def get_tag(content):
    with open('./tag.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['project name', 'project url', 'versions', '#versions'])
        for line in content:
            con = line.split(',')
            pro_path = con[0]
            pro_name = con[1]
            os.chdir(pro_path)

            tag = os.popen('git tag').read().split('\n')
            tags = '?'.join(tag)

            writer.writerow([pro_name, pro_path, tags, len(tag)])


def evaluate(content, writer):
    info = list()
    for line in content:
        con = line.split(',')
        pro_path = con[0]
        pro_name = con[1]
        vers = con[2].replace('\n', '').split('?')
        base_path = './data/' + pro_name + '-enre-out'
        os.makedirs(base_path, exist_ok=True)
        for index in range(0, len(vers)):
            # for index in range(0, 2):
            # 可维护性评估
            tmp_pro, loc, m_num, c_num, me_num = measure_package_metrics(pro_name, pro_path, '',
                                                                         base_path, vers[index],
                                                                         dict(), 'sv')
            res = [pro_name, vers[index], loc, m_num, c_num, me_num]
            res.extend(tmp_pro)
            writer.writerow(res)
        info.append([base_path, vers, pro_path, pro_name])
    return info


def identify(info, identify_res):
    for item in info:
        diff_path = compare_diff(os.path.join(item[0], item[1][0]), os.path.join(item[0], item[1][1]), dict(), item[0])
        cause_path, causes_to_entities = analyse_data(diff_path, item[0], 'others')
        count_list = list()
        count_list.append(item[3])
        count_list.append(item[1][1])
        com_count(count_list, causes_to_entities)
        identify_res.append(count_list)
        # com_mc(item[2], '?'.join(item[1][2:]), cause_path, item[0])


def com_count(count_list, causes_to_entities):
    pass
    # df = pd.DataFrame(causes_to_entities, columns=['type', 'reason', 'module_name', 'class_name', 'method_name'])
    # coupling_df = df.loc[df['type'] == 'coupling']
    # coupling_module_count = len(
    #     coupling_df.drop_duplicates(subset='module_name', keep='first', inplace=False, ignore_index=False))
    # coupling_class_count = len(
    #     coupling_df.drop_duplicates(subset='class_name', keep='first', inplace=False, ignore_index=False))
    # coupling_method_count = len(
    #     coupling_df.drop_duplicates(subset='method_name', keep='first', inplace=False, ignore_index=False))
    # cohesion_df = df.loc[df['type'] == 'cohesion']
    # cohesion_module_count = len(
    #     cohesion_df.drop_duplicates(subset='module_name', keep='first', inplace=False, ignore_index=False))
    # cohesion_class_count = len(
    #     cohesion_df.drop_duplicates(subset='class_name', keep='first', inplace=False, ignore_index=False))
    # cohesion_method_count = len(
    #     cohesion_df.drop_duplicates(subset='method_name', keep='first', inplace=False, ignore_index=False))
    # functionality_df = df.loc[df['type'] == 'functionality']
    # functionality_module_count = len(
    #     functionality_df.drop_duplicates(subset='module_name', keep='first', inplace=False, ignore_index=False))
    # functionality_class_count = len(
    #     functionality_df.drop_duplicates(subset='class_name', keep='first', inplace=False, ignore_index=False))
    # complexity_df = df.loc[df['type'] == 'complexity']
    # complexity_module_count = len(
    #     complexity_df.drop_duplicates(subset='module_name', keep='first', inplace=False, ignore_index=False))
    # evolution_df = df.loc[df['type'] == 'evolution']
    # evolution_module_count = len(
    #     evolution_df.drop_duplicates(subset='module_name', keep='first', inplace=False, ignore_index=False))
    #
    # all_module_count = len(
    #     df.drop_duplicates(subset='module_name', keep='first', inplace=False, ignore_index=False))
    # all_class_count = len(
    #     df.drop_duplicates(subset='class_name', keep='first', inplace=False, ignore_index=False))
    # all_method_count = len(
    #     df.drop_duplicates(subset='method_name', keep='first', inplace=False, ignore_index=False))
    # count_list.extend([coupling_module_count, coupling_class_count, coupling_method_count, cohesion_module_count,
    #                    cohesion_class_count, cohesion_method_count, functionality_module_count,
    #                    functionality_class_count, complexity_module_count, evolution_module_count, all_module_count,
    #                    all_class_count, all_method_count])


def count_file_loc_commit():
    with open('./projects.txt', encoding='utf-8') as file:
        content = file.readlines()
    with open('./count.csv.', 'w', encoding='UTF8', newline='') as file1:
        writer = csv.writer(file1)
        writer.writerow(['project name', 'version', 'loc', '#files', '#commits'])
        for line in content:
            tmp = line.split(',')
            project_path = tmp[0]
            pro_name = tmp[1]
            ver = tmp[2]
            os.chdir(project_path)
            os.system("git checkout -f " + ver)

            # 统计代码行和文件数
            # loc_count = os.popen('cloc .').read()
            # tmp_loc = loc_count.split('\n')
            # tmp_loc1 = tmp_loc[len(tmp_loc) - 3].split(' ')
            # loc = tmp_loc1[len(tmp_loc1) - 1]
            # file = tmp_loc1[len(tmp_loc1) - 1]
            # 统计commit
            log = subprocess.Popen('git log --numstat --date=iso', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
            log_out = log.communicate()[0].decode().split('\n')
            commit_num = 0
            for log_len in log_out:
                if "commit" in str(log_len):
                    commit_num = commit_num + 1

            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            writer.writerow([pro_name, ver, 'loc', 'file', commit_num])

# if __name__ == '__main__':
#     # count_file_loc_commit()
#     with open('./projects.txt', encoding='utf-8') as file:
#         content = file.readlines()
#     with open('./evaluate.csv', 'w', encoding='UTF8', newline='') as file1:
#         writer = csv.writer(file1)
#         head_name = ['project name', 'version', 'score', 'loc', '#modules', '#classes', '#methods']
#         head_name.extend(PROJECT_METRICS)
#         writer.writerow(head_name)
#         info = evaluate(content, writer)
#     with open('./identify.csv.', 'w', encoding='UTF8', newline='') as file2:
#         writer = csv.writer(file2)
#         writer.writerow(
#             ['project name', 'version', '#coupling-probelm-modules',
#              '#coupling-probelm-classes', '#coupling-probelm-methods', '#cohesion-probelm-modules',
#              '#cohesion-probelm-classes', '#cohesion-probelm-methods', '#functionality-probelm-modules',
#              '#functionality-probelm-classes', '#complexity-probelm-modules', '#evolution-probelm-modules',
#              '#all-probelm-modules', '#all-probelm-classes', '#all-probelm-methods'])
#         identify_res = list()
#         # info = list()
#         # info.append([r'G:\实验结果\android\lineage-out',
#         #              ['d56f59389212df5462b342be7600c1974d27c0d5', 'f5600fff5c1fe764b568c7c885eb1aee022a81ca'],
#         #              r'G:\dataset1\AOSP\projects\LineageOS\base',
#         #              'LineageOS'])
#         identify(info, identify_res)
#         writer.writerows(identify_res)
