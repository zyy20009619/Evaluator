# coding=utf-8
import os
import shutil
import csv
import pandas as pd
from function_file import measure_package_metrics, compare_diff
from detect_algo.detect_root_cause import analyse_data
from arch_debt.measure_arch import com_mc


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
        for index in range(0, 1):
            # 可维护性评估
            score, loc, m_num, c_num, me_num = measure_package_metrics(pro_name, pro_path,
                                                                       base_path, vers[index],
                                                                       dict(), 'sv')
            writer.writerow([pro_name, vers[index], score, loc, m_num, c_num, me_num])
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
    df = pd.DataFrame(causes_to_entities, columns=['type', 'module_name', 'class_name', 'method_name'])
    coupling_df = df.loc[df['type'] == 'coupling']
    coupling_module_count = len(
        coupling_df.drop_duplicates(subset='module_name', keep='first', inplace=False, ignore_index=False))
    coupling_class_count = len(
        coupling_df.drop_duplicates(subset='class_name', keep='first', inplace=False, ignore_index=False))
    coupling_method_count = len(
        coupling_df.drop_duplicates(subset='method_name', keep='first', inplace=False, ignore_index=False))
    cohesion_df = df.loc[df['type'] == 'cohesion']
    cohesion_module_count = len(
        cohesion_df.drop_duplicates(subset='module_name', keep='first', inplace=False, ignore_index=False))
    cohesion_class_count = len(
        cohesion_df.drop_duplicates(subset='class_name', keep='first', inplace=False, ignore_index=False))
    cohesion_method_count = len(
        cohesion_df.drop_duplicates(subset='method_name', keep='first', inplace=False, ignore_index=False))
    functionality_df = df.loc[df['type'] == 'functionality']
    functionality_module_count = len(
        functionality_df.drop_duplicates(subset='module_name', keep='first', inplace=False, ignore_index=False))
    functionality_class_count = len(
        functionality_df.drop_duplicates(subset='class_name', keep='first', inplace=False, ignore_index=False))
    complexity_df = df.loc[df['type'] == 'complexity']
    complexity_module_count = len(
        complexity_df.drop_duplicates(subset='module_name', keep='first', inplace=False, ignore_index=False))
    evolution_df = df.loc[df['type'] == 'evolution']
    evolution_module_count = len(
        evolution_df.drop_duplicates(subset='module_name', keep='first', inplace=False, ignore_index=False))

    all_module_count = len(
        df.drop_duplicates(subset='module_name', keep='first', inplace=False, ignore_index=False))
    all_class_count = len(
        df.drop_duplicates(subset='class_name', keep='first', inplace=False, ignore_index=False))
    all_method_count = len(
        df.drop_duplicates(subset='method_name', keep='first', inplace=False, ignore_index=False))
    count_list.extend([coupling_module_count, coupling_class_count, coupling_method_count, cohesion_module_count,
                       cohesion_class_count, cohesion_method_count, functionality_module_count,
                       functionality_class_count, complexity_module_count, evolution_module_count, all_module_count,
                       all_class_count, all_method_count])


if __name__ == '__main__':
    with open('./projects.txt', encoding='utf-8') as file:
        content = file.readlines()
    with open('./evaluate.csv.', 'w', encoding='UTF8', newline='') as file1:
        writer = csv.writer(file1)
        writer.writerow(['project name', 'version', 'score', 'loc', '#modules', '#classes', '#methods'])
        info = evaluate(content, writer)
    # with open('./identify.csv.', 'w', encoding='UTF8', newline='') as file2:
    #     writer = csv.writer(file2)
    #     writer.writerow(
    #         ['project name', 'version', '#coupling-probelm-modules',
    #          '#coupling-probelm-classes', '#coupling-probelm-methods', '#cohesion-probelm-modules',
    #          '#cohesion-probelm-classes', '#cohesion-probelm-methods', '#functionality-probelm-modules',
    #          '#functionality-probelm-classes', '#complexity-probelm-modules', '#evolution-probelm-modules',
    #          '#all-probelm-modules', '#all-probelm-classes', '#all-probelm-methods'])
    #     identify_res = list()
    #     identify(info, identify_res)
    #     writer.writerows(identify_res)
