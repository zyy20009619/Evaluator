import os

import pandas as pd
from xml.dom.minidom import parse
from arch_debt.maintenance_cost_measurement.changeproness import *
from arch_debt.maintenance_cost_measurement.gitlogprocessor import *
from util.csv_operator import write_to_csv, read_csv, read_csv_to_pd
from util.path_operator import create_dir_path
from util.json_operator import read_file
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score


# 计算每个项目(取最新版本)的gt(三个指标)及其阈值，求精确率等
def com_aarf(vers, pro_name, mc_list):
    versions = vers.split('?')
    # ths = th.split(';')  # #auth/#cmt/#cChurn
    # gt
    files, auth, cmt, cChurn = get_gt(pro_name, versions)
    # ours
    print('pro_name:', pro_name)
    print('ours:')
    sample = get_ours(pro_name, files, 'ours')
    get_metric(auth, cmt, cChurn, sample, mc_list, 'ours', pro_name)
    # dv8
    print('dv8:')
    sample = get_dv8(pro_name, files, 'dv8')
    get_metric(auth, cmt, cChurn, sample, mc_list, 'dv8', pro_name)
    # designite
    print('designite:')
    sample = get_designite(pro_name, files, 'designite')
    get_metric(auth, cmt, cChurn, sample, mc_list, 'designite', pro_name)
    # designite


def get_designite(pro_name, files, method):
    compare_base_path = r'D:\paper-data-and-result\results\bishe-results\mc-result\Designite-results'
    design_file_path = compare_base_path + '/' + pro_name + '/designCodeSmells.csv'
    implementation_file_path = compare_base_path + '/' + pro_name + '/implementationCodeSmells.csv'

    design_pd = read_csv_to_pd(design_file_path)
    design_pd = design_pd[['Package Name', 'Type Name']]
    design_pd['Type Name'] = design_pd.apply(lambda x: x['Package Name'] + "." + x['Type Name'], axis=1)

    implementation_pd = read_csv_to_pd(implementation_file_path)
    implementation_pd = implementation_pd[['Package Name', 'Type Name']]
    implementation_pd['Type Name'] = implementation_pd.apply(lambda x: x['Package Name'] + "." + x['Type Name'],
                                                             axis=1)

    designite_pd = pd.concat([design_pd, implementation_pd], axis=0).reset_index(drop=True)
    return get_sample_dis(files, set(designite_pd['Type Name']), method)


def get_metric(auth, cmt, cChurn, sample, mc_list, tool, pro_name):
    auth_label = pd.merge(auth, sample, how='inner', on='filename')
    cmt_label = pd.merge(cmt, sample, how='inner', on='filename')
    cChurn_label = pd.merge(cChurn, sample, how='inner', on='filename')
    print('auth:')
    get_metrics(auth_label, mc_list, pro_name, tool, '#auth')
    print('cmt:')
    get_metrics(cmt_label, mc_list, pro_name, tool, '#cmt')
    print('cChurn:')
    get_metrics(cChurn_label, mc_list, pro_name, tool, '#cChurn')


def get_dv8(pro_name, files, method):
    dv8_base_path = r'D:\paper-data-and-result\results\bishe-results\mc-result\dv8-results'
    file_path = dv8_base_path + '/' + pro_name + '/dv8-analysis-result/file-measure-report.csv'
    dv8_pd = read_csv_to_pd(file_path)
    pf_pd = dv8_pd[
        ['FileName', 'numCrossing', 'numModularityViolation', 'numPackageCycle', 'numUnhealthyInheritance',
         'numUnstableInterface', 'numClique']]
    crossing_files = pf_pd[pf_pd['numCrossing'] != 0]['FileName']
    modularity_violation_files = pf_pd[pf_pd['numModularityViolation'] != 0]['FileName']
    package_cycle_files = pf_pd[pf_pd['numPackageCycle'] != 0]['FileName']
    unhealthy_inheritance_files = pf_pd[pf_pd['numUnhealthyInheritance'] != 0]['FileName']
    unstable_interface_files = pf_pd[pf_pd['numUnstableInterface'] != 0]['FileName']
    clique_files = pf_pd[pf_pd['numClique'] != 0]['FileName']

    all_pf_files = pd.concat(
        [crossing_files, modularity_violation_files, package_cycle_files, unhealthy_inheritance_files,
         unstable_interface_files, clique_files], axis=0).reset_index(drop=True)
    return get_sample_dis(files, set(all_pf_files), method)


def get_metrics(label, mc_list, pro_name, tool, mc_metric):
    TP = len(label[(label['label_pre'] == 1) & (label['label'] == 1)])
    FP = len(label[(label['label_pre'] == 1) & (label['label'] == 0)])
    FN = len(label[(label['label_pre'] == 0) & (label['label'] == 1)])
    TN = len(label[(label['label_pre'] == 0) & (label['label'] == 0)])
    # 计算Precision
    print('Precision:', precision_score(label['label'], label['label_pre']))
    # 计算Recall
    print('Recall:', recall_score(label['label'], label['label_pre']))
    # 计算Accuracy
    print('Accuracy:', accuracy_score(label['label'], label['label_pre']))
    # 计算F1
    print('F1:', f1_score(label['label'], label['label_pre']))
    mc_list.append([pro_name, tool, mc_metric, precision_score(label['label'], label['label_pre']),
                    recall_score(label['label'], label['label_pre']),
                    accuracy_score(label['label'], label['label_pre']), f1_score(label['label'], label['label_pre'])])


def get_gt(pro_name, versions):
    # 第一种ground-truth：历史中的维护数据
    return get_history_gt(pro_name, versions)
    # 第二种ground-truth：结构中的维护成本较高


def get_struct_gt(pro_name, pro_path, versions, mc_list):
    versions = versions.split('?')
    os.chdir(pro_path)
    os.system('git checkout -f ' + versions[0])
    struct_path = 'D:\\paper-data-and-result\\results\\paper-results\mv\\' + pro_name + '-enre-out\\' + versions[0]
    struct_res = read_csv_to_pd(os.path.join(struct_path, 'measure_result_class.csv'))
    struct_res = struct_res[['class_name', 'CBC']]
    path_name = get_all_files_by_filter(pro_path, struct_res['class_name'])
    path_name = pd.merge(struct_res, path_name, how='inner', on='class_name')
    path_name.sort_values(by='CBC', inplace=True, ascending=False)

    gt_file_number = 40
    print('file number:', len(path_name))
    print('gt file number:', gt_file_number)
    path_name1 = path_name.iloc[0:gt_file_number]
    path_name1['label'] = 1
    path_name2 = path_name.iloc[gt_file_number:]
    path_name2['label'] = 0
    path_name = pd.concat([path_name1, path_name2])
    # ours
    print('pro_name:', pro_name)
    print('ours:')
    sample = get_ours(pro_name, path_name['filename'], 'ours')
    sample = pd.merge(path_name, sample, how='inner', on='filename')
    get_metrics(sample, mc_list, pro_name, 'ours', 'struct')
    # dv8
    print('dv8:')
    sample = get_dv8(pro_name, path_name['filename'], 'dv8')
    sample = pd.merge(path_name, sample, how='inner', on='filename')
    get_metrics(sample, mc_list, pro_name, 'dv8', 'struct')
    # designite
    print('designite:')
    sample = get_designite(pro_name, path_name['filename'], 'designite')
    sample = pd.merge(path_name, sample, how='inner', on='filename')
    get_metrics(sample, mc_list, pro_name, 'designite', 'struct')


def get_main_gt():
    base_path = r'D:\paper-data-and-result\results\bishe-results\mc-result\labels.csv'
    gt_res = read_csv_to_pd(base_path)[['projectname', 'path', 'overall']]
    argouml = gt_res[gt_res['projectname'] == 'argouml']['overall']
    print(argouml)

# if __name__ == '__main__':
#     get_main_gt()


def get_all_files_by_filter(project_path, quali_name):
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
    path = _format_file_path(file_list_java, quali_name)
    path_name = pd.DataFrame(data=path, columns=['filename', 'class_name'])
    return path_name

def get_history_gt(pro_name, versions):
    detect_path = 'D:\paper-data-and-result\\results\\bishe-results\\mc-result\\dbMIT-results\\' + pro_name + '\\analyseResult0.6'
    detection_res = read_csv_to_pd(os.path.join(detect_path, 'detection result.csv'))
    detection_res = set(detection_res['problem class'])
    # 读gt，整理所有文件，满足阈值条件的标记为1，不满足阈值条件的标记为0
    base_version_path = os.path.join(os.path.join(r'D:\paper-data-and-result\results\paper-results\mv',
                                                  pro_name + '-enre-out'),
                                     'mc/' + versions[len(versions) - 1].replace('\n', ''))
    gt_path = read_csv_to_pd(os.path.join(base_version_path, 'file mc.csv'))
    # 取前5%为高维护成本文件
    gt_file_number = 20
    # gt_file_number = len(detection_res)
    # gt_file_number = int(len(gt_path) * 0.03)
    # gt_file_number = int(len(gt_path) * 0.1)
    # gt_file_number = int(len(gt_path) * 0.05)
    print('file number:', len(gt_path))
    print('gt file number:', gt_file_number)
    # 分别读#author、#cmt、#changeloc，划分真正正例和负例
    author_pd = gt_path[['filename', '#author']]
    author_pd.sort_values(by="#author", inplace=True, ascending=False)
    # auth_true_pd = author_pd[author_pd['#author'] > int(ths[0])]
    auth_true_pd = author_pd.iloc[0:gt_file_number]
    auth_true_pd['label'] = 1
    # auth_false_pd = author_pd[author_pd['#author'] <= int(ths[0])]
    auth_false_pd = author_pd.iloc[gt_file_number:]
    auth_false_pd['label'] = 0
    auth = pd.concat([auth_true_pd, auth_false_pd])
    cmt_pd = gt_path[['filename', '#cmt']]
    cmt_pd.sort_values(by="#cmt", inplace=True, ascending=False)
    # cmt_true_pd = cmt_pd[cmt_pd['#cmt'] > int(ths[1])]
    cmt_true_pd = cmt_pd.iloc[0:gt_file_number]
    cmt_true_pd['label'] = 1
    # cmt_false_pd = cmt_pd[cmt_pd['#cmt'] <= int(ths[1])]
    cmt_false_pd = cmt_pd.iloc[gt_file_number:]
    cmt_false_pd['label'] = 0
    cmt = pd.concat([cmt_true_pd, cmt_false_pd])
    changeloc_pd = gt_path[['filename', '#changeloc']]
    changeloc_pd.sort_values(by="#changeloc", inplace=True, ascending=False)
    # changeloc_true_pd = changeloc_pd[changeloc_pd['#changeloc'] > int(ths[2])]
    changeloc_true_pd = changeloc_pd.iloc[0:gt_file_number]
    changeloc_true_pd['label'] = 1
    # changeloc_false_pd = changeloc_pd[changeloc_pd['#changeloc'] <= int(ths[2])]
    changeloc_false_pd = changeloc_pd.iloc[gt_file_number:]
    changeloc_false_pd['label'] = 0
    changeloc = pd.concat([changeloc_true_pd, changeloc_false_pd])
    return gt_path['filename'], auth, cmt, changeloc


def get_ours(pro_name, files, method):
    detect_path = 'D:\paper-data-and-result\\results\\bishe-results\\mc-result\\dbMIT-results\\' + pro_name + '\\analyseResult0.6'
    detection_res = read_csv_to_pd(os.path.join(detect_path, 'detection result.csv'))
    detection_res = set(detection_res['problem class'])
    return get_sample_dis(files, detection_res, method)


def get_sample_dis(files, pf_entities, method):
    # 为所有文件分类：预测为正样本和预测为负样本
    pos_files = list()
    for pf_entity in pf_entities:
        for file in files:
            if method == 'ours' or method == 'designite':
                if pf_entity.replace('.', '/') in file:
                    pos_files.append(file)
            elif method == 'dv8':
                if pf_entity in file:
                    pos_files.append(file)
    pos_pd = pd.DataFrame(data=pos_files, columns=['filename'])
    pos_pd['label_pre'] = 1
    neg_files = set(files) - set(pos_files)
    neg_pd = pd.DataFrame(data=list(neg_files), columns=['filename'])
    neg_pd['label_pre'] = 0
    sample = pd.concat([pos_pd, neg_pd])
    return sample


# 计算gt每个版本和方法中被识别出的top交集(暂不使用此种方案)
def com_inter(project_path, vers, pro_name, method, top_ver):
    versions = vers.split('?')
    # ours
    detect_path = 'D:\paper-data-and-result\\results\\bishe-results\\mc-result\\dbMIT-results\\' + pro_name + '\\analyseResult0.6'
    detection_res = read_csv_to_pd(os.path.join(detect_path, 'detection result.csv'))
    detection_res.sort_values(by="class decay degree", inplace=True, ascending=False)
    detection_res.drop_duplicates(subset=['problem class'], keep='first', inplace=True)
    # dv8
    base_out_path = r'E:\results\bishe-results\mc-result\dbMIT-results' + '\\' + pro_name + '\\' + \
                    versions[0]
    dep_dic = read_file(os.path.join(base_out_path, pro_name + '-out.json'))
    variables = dep_dic['variables']
    path_to_qualifiedName = list()
    for var in variables:
        if var['category'] == 'File':
            path_to_qualifiedName.append([var['File'], var['qualifiedName'][:-5]])
    file_pd = pd.DataFrame(data=path_to_qualifiedName, columns=['FileName', 'problem class'])
    compare_base_path = r'E:\results\bishe-results\mc-result\dv8-results'
    file_path = compare_base_path + '/' + pro_name + '/dv8-analysis-result/file-measure-report.csv'
    dv8_pd = read_csv_to_pd(file_path)
    pf_pd = dv8_pd[
        ['FileName', 'numCrossing', 'numModularityViolation', 'numPackageCycle', 'numUnhealthyInheritance',
         'numUnstableInterface', 'numClique']]
    pf_pd = pd.merge(pf_pd, file_pd, how='inner', on=['FileName'])
    del pf_pd['FileName']
    pf_pd['count'] = pf_pd.apply(
        lambda x: (x['numCrossing'] + x['numModularityViolation'] + x['numPackageCycle'] + x[
            'numUnhealthyInheritance'] +
                   x['numUnstableInterface'] + x['numClique']),
        axis=1)
    pf_pd.sort_values(by="count", inplace=True, ascending=False)
    # designite
    compare_base_path = r'E:\results\bishe-results\mc-result\Designite-results'
    design_file_path = compare_base_path + '/' + pro_name + '/designCodeSmells.csv'
    implementation_file_path = compare_base_path + '/' + pro_name + '/implementationCodeSmells.csv'

    design_pd = read_csv_to_pd(design_file_path)
    design_pd = design_pd[['Package Name', 'Type Name']]
    design_pd['Type Name'] = design_pd.apply(lambda x: x['Package Name'] + "." + x['Type Name'], axis=1)

    implementation_pd = read_csv_to_pd(implementation_file_path)
    implementation_pd = design_pd[['Package Name', 'Type Name']]
    implementation_pd['Type Name'] = implementation_pd.apply(lambda x: x['Package Name'] + "." + x['Type Name'],
                                                             axis=1)

    designite_pd = pd.concat([design_pd, implementation_pd], axis=0).reset_index(drop=True)
    designite_list = [list(designite_pd["Type Name"].value_counts().index),
                      list(designite_pd["Type Name"].value_counts())]
    designite_list = [[row[i] for row in designite_list] for i in range(len(designite_list[0]))]
    designite_pd = pd.DataFrame(data=designite_list, columns=['problem class', 'degree'])
    for version in versions[1:]:
        tmp_top_ver = list()
        version = version.replace('\n', '')
        tmp_top_ver.append(pro_name)
        tmp_top_ver.append(version)
        # 读gt
        base_version_path = os.path.join(os.path.join(r'E:\results\paper-results\mv',
                                                      pro_name + '-enre-out'),
                                         'mc/' + version)
        gt_path = read_csv_to_pd(os.path.join(base_version_path, 'file mc.csv'))
        # 分别读#author、#cmt、#changeloc，然后按照从大到小排序
        author_pd = gt_path[['filename', '#author']]
        author_pd.sort_values(by="#author", inplace=True, ascending=False)
        cmt_pd = gt_path[['filename', '#cmt']]
        cmt_pd.sort_values(by="#cmt", inplace=True, ascending=False)
        changeloc_pd = gt_path[['filename', '#changeloc']]
        changeloc_pd.sort_values(by="#changeloc", inplace=True, ascending=False)
        get_inter(tmp_top_ver, detection_res, gt_path, author_pd, cmt_pd, changeloc_pd)
        get_inter(tmp_top_ver, pf_pd, gt_path, author_pd, cmt_pd, changeloc_pd)
        get_inter(tmp_top_ver, designite_pd, gt_path, author_pd, cmt_pd, changeloc_pd)
        top_ver.append(tmp_top_ver)


def get_inter(tmp_top_ver, detection_res, gt_path, author_pd, cmt_pd, changeloc_pd):
    # top1_pf_entities = tmp_format_file_path(gt_path['filename'], detection_res.head(1)['problem class'])
    #
    # print('top1(author):', len(set(top1_pf_entities) & set(author_pd.head(1)['filename'])))
    # print('top1(cmt):', len(set(top1_pf_entities) & set(cmt_pd.head(1)['filename'])))
    # print('top1(changeloc):', len(set(top1_pf_entities) & set(changeloc_pd.head(1)['filename'])))
    # top3_pf_entities = tmp_format_file_path(gt_path['filename'], detection_res.head(3)['problem class'])
    #
    # print('top3(author):', len(set(top3_pf_entities) & set(author_pd.head(3)['filename'])))
    # print('top3(cmt):', len(set(top3_pf_entities) & set(cmt_pd.head(3)['filename'])))
    # print('top3(changeloc):', len(set(top3_pf_entities) & set(changeloc_pd.head(3)['filename'])))
    top5_pf_entities = tmp_format_file_path(gt_path['filename'], detection_res.head(5)['problem class'])

    print('top5(author):', len(set(top5_pf_entities) & set(author_pd.head(5)['filename'])))
    print('top5(cmt):', len(set(top5_pf_entities) & set(cmt_pd.head(5)['filename'])))
    print('top5(changeloc):', len(set(top5_pf_entities) & set(changeloc_pd.head(5)['filename'])))

    # top10_pf_entities = tmp_format_file_path(gt_path['filename'], detection_res.head(10)['problem class'])
    #
    # print('top10(author):', len(set(top10_pf_entities) & set(author_pd.head(10)['filename'])))
    # print('top10(cmt):', len(set(top10_pf_entities) & set(cmt_pd.head(10)['filename'])))
    # print('top10(changeloc):', len(set(top10_pf_entities) & set(changeloc_pd.head(10)['filename'])))
    #
    # top50_pf_entities = tmp_format_file_path(gt_path['filename'], detection_res.head(50)['problem class'])
    #
    # print('top50(author):', len(set(top50_pf_entities) & set(author_pd.head(50)['filename'])))
    # print('top50(cmt):', len(set(top50_pf_entities) & set(cmt_pd.head(50)['filename'])))
    # print('top50(changeloc):', len(set(top50_pf_entities) & set(changeloc_pd.head(50)['filename'])))

    # tmp_top_ver.extend([len(set(top10_pf_entities) & set(author_pd.head(10)['filename'])),
    #                     len(set(top50_pf_entities) & set(author_pd.head(50)['filename'])),
    #                     len(set(top10_pf_entities) & set(cmt_pd.head(10)['filename'])),
    #                     len(set(top50_pf_entities) & set(cmt_pd.head(50)['filename'])),
    #                     len(set(top10_pf_entities) & set(changeloc_pd.head(10)['filename'])),
    #                     len(set(top50_pf_entities) & set(changeloc_pd.head(50)['filename']))])
    tmp_top_ver.extend([len(set(top5_pf_entities) & set(author_pd.head(5)['filename'])),
                        len(set(top5_pf_entities) & set(cmt_pd.head(5)['filename'])),
                        len(set(top5_pf_entities) & set(changeloc_pd.head(5)['filename']))])
    # tmp_top_ver.extend([len(set(top3_pf_entities) & set(author_pd.head(3)['filename'])),
    #                     len(set(top3_pf_entities) & set(cmt_pd.head(3)['filename'])),
    #                     len(set(top3_pf_entities) & set(changeloc_pd.head(3)['filename']))])
    # tmp_top_ver.extend([len(set(top1_pf_entities) & set(author_pd.head(1)['filename'])),
    #                     len(set(top1_pf_entities) & set(cmt_pd.head(1)['filename'])),
    #                     len(set(top1_pf_entities) & set(changeloc_pd.head(1)['filename']))])


def tmp_format_file_path(filenames, pf_entities):
    result = list()
    for pf_entity in pf_entities:
        for file in filenames:
            if pf_entity.replace('.', '\\') in file:
                result.append(file)
                break
    return result


def com_mc(project_path, vers, pro_name, method, files, our_pf_files, tmp_gt):
    print(method)
    # causes_entities = read_csv(cause_path, 'causes_entities.csv')
    if method == 'ours':
        versions = vers.split('?')
        os.chdir(project_path)
        os.system('git checkout -f ' + versions[0])
        files = get_all_files_by_filter(project_path, list())
        print('file_number:', len(files))
        detect_path = 'D:\paper-data-and-result\\results\\bishe-results\\mc-result\\dbMIT-results\\' + pro_name + '\\analyseResult0.6'
        detection_res = read_csv_to_pd(os.path.join(detect_path, 'detection result.csv'))
        # pf_entities = _format_file_path(files, list(
        #     set(detection_res[detection_res['class status'] != 'delete']['problem class'])))
        # print('ours:', len(pf_entities))
        # print('ours(总比率):', len(pf_entities) / len(files))
        # pd_df = pd.DataFrame(data=pf_entities, columns=['class'])
        measure_maintenance(project_path,
                            detection_res[detection_res['class status'] != 'delete']['problem class'], versions[1:],
                            detect_path, pro_name, tmp_gt)
        return files
    elif method == 'dv8':
        extract_dv8_pf_files(project_path, vers, pro_name, files, our_pf_files)
    elif method == 'tc':
        extract_tc_pf_files(project_path, vers, pro_name)
    elif method == 'arcade':
        extract_arcade_pf_files(project_path, vers, pro_name, files, our_pf_files)
    elif method == 'designite':
        extract_designite_pf_files(project_path, vers, pro_name, files, our_pf_files)


# def get_all_files_by_filter(project_path):
#     file_list_java = list()
#     for filename, dirs, files in os.walk(project_path, topdown=True):
#         filename = filename.split(project_path)[1]
#         filename = filename.replace("\\", "/")
#         if filename.startswith(".git") or filename.startswith(".github"):
#             continue
#         for file in files:
#             file_temp = filename + "\\" + file
#             file_temp = file_temp[1:]
#             file_temp = file_temp.replace("\\", "/")
#             if file.endswith(".java"):
#                 file_list_java.append(file_temp)
#     return file_list_java


def extract_designite_pf_files(project_path, vers, pro_name, files, our_pf_files):
    versions = vers.split('?')
    compare_base_path = r'E:\results\bishe-results\mc-result\Designite-results'
    design_file_path = compare_base_path + '/' + pro_name + '/designCodeSmells.csv'
    implementation_file_path = compare_base_path + '/' + pro_name + '/implementationCodeSmells.csv'

    design_pd = read_csv_to_pd(design_file_path)
    design_pd = design_pd[['Package Name', 'Type Name']]
    design_pd['Type Name'] = design_pd.apply(lambda x: x['Package Name'] + "." + x['Type Name'], axis=1)

    implementation_pd = read_csv_to_pd(implementation_file_path)
    implementation_pd = design_pd[['Package Name', 'Type Name']]
    implementation_pd['Type Name'] = implementation_pd.apply(lambda x: x['Package Name'] + "." + x['Type Name'],
                                                             axis=1)

    pf_pd = pd.concat([design_pd, implementation_pd], axis=0).reset_index(drop=True)
    # pf_entities = _format_file_path(files, list(set(pf_pd['Type Name'])))
    # print('Designite:', len(pf_entities))
    # print('Designite(总比率):', len(pf_entities) / len(files))
    # print('Designite:', len(set(pf_entities) & our_pf_files))
    # print('Designite(交集比率):', (len(set(pf_entities) & our_pf_files)) / len(our_pf_files))
    # 计算维护成本
    measure_maintenance(project_path, pf_pd['Type Name'], versions[1:],
                        create_dir_path(os.path.join(compare_base_path, pro_name)), pro_name)


def extract_arcade_pf_files(project_path, vers, pro_name, files, our_pf_files):
    versions = vers.split('?')
    compare_base_path = r'E:\results\bishe-results\mc-result\\ARCADE-results'
    file_path = compare_base_path + '/' + pro_name + '/smells.xml'
    if not os.path.exists(file_path):
        return
    dom = parse(file_path)
    # 获取文件元素对象
    document = dom.documentElement
    # 读取配置文件中ipinfo数据
    entities = document.getElementsByTagName("string")
    pf_entities = list()
    for entity in entities:
        pf_entities.append(entity.childNodes[0].data)
    # print(set(pf_entities))
    pf_files = pd.DataFrame(data=pf_entities, columns=['class'])
    # pf_entities = _format_file_path(files, list(set(pf_files['class'])))
    # print('ARCADE:', len(pf_entities))
    # print('ARCADE(总比率):', len(pf_entities) / len(files))
    # print('ARCADE:', len(set(pf_entities) & our_pf_files))
    # print('ARCADE(交集比率):', (len(set(pf_entities) & our_pf_files)) / len(our_pf_files))
    # 计算维护成本
    measure_maintenance(project_path, pf_files['class'], versions[1:],
                        create_dir_path(os.path.join(compare_base_path, pro_name)), pro_name)


# 这条路走不通
def extract_tc_pf_files(project_path, vers, pro_name):
    versions = vers.split('?')
    # 将dv8识别的文件名结果转化为qualifiedName
    base_out_path = r'E:\results\bishe-results\mc-result\dbMIT-results' + '\\' + pro_name + '\\' + \
                    versions[0]
    dep_dic = read_file(os.path.join(base_out_path, pro_name + '-out.json'))
    variables = dep_dic['variables']
    path_to_qualifiedName = list()
    for var in variables:
        if var['category'] == 'File':
            path_to_qualifiedName.append([var['File'], var['qualifiedName'][:-5]])
    file_pd = pd.DataFrame(data=path_to_qualifiedName, columns=['class_path', 'qualifiedName'])

    compare_base_path = r'E:\results\bishe-results\mc-result\TDClassifier-results'
    file_path = compare_base_path + '/' + pro_name + '/results.csv'
    tc_pd = read_csv_to_pd(file_path)
    pf_pd = tc_pd[['class_path', 'high_td']]
    pf_pd = pd.merge(pf_pd, file_pd, how='inner', on=['class_path'])
    del pf_pd['class_path']
    high_td_files = pf_pd[pf_pd['high_td'] == 1]['qualifiedName']

    # 计算维护成本
    measure_maintenance(project_path, high_td_files, versions[1:],
                        create_dir_path(os.path.join(compare_base_path, pro_name)), pro_name)


def extract_dv8_pf_files(project_path, vers, pro_name, files, our_pf_files):
    versions = vers.split('?')
    # 将dv8识别的文件名结果转化为qualifiedName
    base_out_path = r'D:\paper-data-and-result\results\bishe-results\mc-result\dbMIT-results' + '\\' + pro_name + '\\' + \
                    versions[0]
    dep_dic = read_file(os.path.join(base_out_path, pro_name + '-out.json'))
    variables = dep_dic['variables']
    path_to_qualifiedName = list()
    for var in variables:
        if var['category'] == 'File':
            path_to_qualifiedName.append([var['File'], var['qualifiedName'][:-5]])
    file_pd = pd.DataFrame(data=path_to_qualifiedName, columns=['FileName', 'qualifiedName'])

    compare_base_path = r'D:\paper-data-and-result\results\bishe-results\mc-result\dv8-results'
    file_path = compare_base_path + '/' + pro_name + '/dv8-analysis-result/file-measure-report.csv'
    dv8_pd = read_csv_to_pd(file_path)
    pf_pd = dv8_pd[
        ['FileName', 'numCrossing', 'numModularityViolation', 'numPackageCycle', 'numUnhealthyInheritance',
         'numUnstableInterface', 'numClique']]
    pf_pd = pd.merge(pf_pd, file_pd, how='inner', on=['FileName'])
    del pf_pd['FileName']
    # pf_pd.replace('/', '\\', inplace=True)
    crossing_files = pf_pd[pf_pd['numCrossing'] != 0]['qualifiedName']
    modularity_violation_files = pf_pd[pf_pd['numModularityViolation'] != 0]['qualifiedName']
    package_cycle_files = pf_pd[pf_pd['numPackageCycle'] != 0]['qualifiedName']
    unhealthy_inheritance_files = pf_pd[pf_pd['numUnhealthyInheritance'] != 0]['qualifiedName']
    unstable_interface_files = pf_pd[pf_pd['numUnstableInterface'] != 0]['qualifiedName']
    clique_files = pf_pd[pf_pd['numClique'] != 0]['qualifiedName']

    all_pf_files = pd.concat(
        [crossing_files, modularity_violation_files, package_cycle_files, unhealthy_inheritance_files,
         unstable_interface_files, clique_files], axis=0).reset_index(drop=True)
    # pf_entities = _format_file_path(files, list(set(all_pf_files)))
    # print('DV8:', len(pf_entities))
    # print('DV8(总比率):', len(pf_entities) / len(files))
    # print('DV8:', len(set(pf_entities) & our_pf_files))
    # print('DV8(交集比率):', (len(set(pf_entities) & our_pf_files)) / len(our_pf_files))
    # 计算维护成本
    # measure_maintenance(project_path, crossing_files, versions[1:],
    #                     create_dir_path(os.path.join(compare_base_path,
    #                                  pro_name + '\crossing')), pro_name)
    # measure_maintenance(project_path, modularity_violation_files, versions[1:],
    #                     create_dir_path(os.path.join(compare_base_path,
    #                                  pro_name + '\cmodularity_violation')), pro_name)
    # measure_maintenance(project_path, package_cycle_files, versions[1:],
    #                     create_dir_path(os.path.join(compare_base_path,
    #                                  pro_name + '\package_cycle')), pro_name)
    # measure_maintenance(project_path, unhealthy_inheritance_files, versions[1:],
    #                     create_dir_path(os.path.join(compare_base_path,
    #                                  pro_name + '\\unhealthy_inheritance')), pro_name)
    # measure_maintenance(project_path, unstable_interface_files, versions[1:],
    #                     create_dir_path(os.path.join(compare_base_path,
    #                                  pro_name + '\\unstable_interface')), pro_name)
    # measure_maintenance(project_path, clique_files, versions[1:],
    #                     create_dir_path(os.path.join(compare_base_path,
    #                                  pro_name + '\clique')), pro_name)
    measure_maintenance(project_path, all_pf_files, versions[1:],
                        create_dir_path(os.path.join(compare_base_path,
                                                     pro_name + '\\all_pf')), pro_name)


def measure_maintenance(project_path, pf_entities, versions, output_path, pro_name, tmp_gt):
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
    gt_mc_list = list()
    # versions = vers.split('?')
    for version in versions:
        version = version.replace('\n', '')
        tmp_gt.append(pro_name)
        tmp_gt.append(version)
        version_mc = list()
        gt_version_mc = list()
        version_mc.append(version)
        gt_version_mc.append(version)
        base_version_path = os.path.join(os.path.join(r'D:\paper-data-and-result\results\paper-results\mv',
                                                      pro_name + '-enre-out'),
                                         'mc/' + version)
        # 获取到该版本的loc和log，计算版本中每个文件的维护成本
        commit_collection_res, file_list_java, file_loc_dict = gitlog(project_path, version, base_version_path)
        # 计算所有文件的维护成本
        all_files_mc_pd, all_cmt, all_loc, all_auth = changeProness(file_list_java, commit_collection_res,
                                                                    create_file_path(base_version_path,
                                                                                     'file mc.csv'), tmp_gt)
        # 计算问题实体和非问题实体的维护成本
        # pf_cmt, pf_loc, pf_auth = com_pfs_mc(all_files_mc_pd, file_loc_dict, pf_entities, version_mc, gt_version_mc)
        mc_list.append(version_mc)
        # gt_version_mc.append(pf_cmt)
        # gt_version_mc.append(all_cmt)
        # gt_version_mc.append(pf_cmt / all_cmt)
        # gt_version_mc.append(pf_loc)
        # gt_version_mc.append(all_loc)
        # gt_version_mc.append(pf_loc / all_loc)
        # gt_version_mc.append(pf_auth)
        # gt_version_mc.append(all_auth)
        # gt_version_mc.append(pf_auth / all_auth)
        # gt_mc_list.append(gt_version_mc)
    res_pf = pd.DataFrame(data=mc_list, columns=['version', '#commit-mc(A)', '#commit-mc(B)', '#commit-average(P)',
                                                 '#changeLoc-mc(A)', '#changeLoc-mc(B)', '#changeLoc-average(P)',
                                                 '#author-mc(A)', '#author-mc(B)', '#author-average(P)'])
    pf_res_pf = pd.DataFrame(data=gt_mc_list, columns=['version', '#pf_cmt', '#all_cmt', '#R_cmt',
                                                       '#pf_loc', '#all_loc', '#R_loc',
                                                       '#pf_author', '#all_author', '#R_author', ])
    res_pf['projectname'] = os.path.basename(project_path)
    pf_res_pf['projectname'] = os.path.basename(project_path)
    res_pf.to_csv(os.path.join(output_path, "mc result.csv"), index=False, sep=',')
    pf_res_pf.to_csv(os.path.join(output_path, "pf mc result.csv"), index=False, sep=',')
    # write_to_csv(cmt_list, out_path + '/mc/causes_cmt.csv')
    # write_to_csv(change_loc_list, out_path + '/mc/causes_change_loc.csv')
    # write_to_csv(author_list, out_path + '/mc/causes_author.csv')
    # 切换回当前工作目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # write_to_csv(issue_list, out_path + '/mc/causes_issue.csv')
    # write_to_csv(issue_cmt_list, out_path + '/mc/causes_issue_cmt.csv')
    # write_to_csv(issue_loc_list, out_path + '/mc/causes_issue_loc.csv')


def com_pfs_mc(all_files_mc_pd, file_loc_dict, pf_entities, version_mc, gt_version_mc):
    # causes_mc_result = list()
    # causes_mc_result.append(['cause', '#author', '#cmt', '#changeloc', '#issue', '#issue-cmt', 'issueLoc'])
    # test_entities = list()
    # 求问题实体维护成本
    pf_entities = _format_file_path(all_files_mc_pd['filename'], pf_entities)
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
            pf_entities_change_loc += list(all_files_mc_pd[all_files_mc_pd['filename'] == pf_entity]['change_loc'])[
                0]
            pf_entities_author.extend(
                list(all_files_mc_pd[all_files_mc_pd['filename'] == pf_entity]['author_id'])[0])
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
            non_pf_entities_cmt.extend(
                list(all_files_mc_pd[all_files_mc_pd['filename'] == non_pf_entity]['cmt_id'])[0])
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
    print('pf_entities_change_loc:', pf_entities_change_loc)
    print('pf_entity_loc_num:', pf_entity_loc_num)
    print('non_pf_entities_change_loc:', non_pf_entities_change_loc)
    print('non_pf_entity_loc_num:', non_pf_entity_loc_num)
    version_mc.extend(
        [len(set(pf_entities_cmt)) / pf_entity_loc_num, len(set(non_pf_entities_cmt)) / non_pf_entity_loc_num,
         (len(set(pf_entities_cmt)) / pf_entity_loc_num) / (len(set(non_pf_entities_cmt)) / non_pf_entity_loc_num),
         pf_entities_change_loc / pf_entity_loc_num, non_pf_entities_change_loc / non_pf_entity_loc_num,
         (pf_entities_change_loc / pf_entity_loc_num) / (non_pf_entities_change_loc / non_pf_entity_loc_num),
         len(set(pf_entities_author)) / pf_entity_loc_num, len(set(non_pf_entities_author)) / non_pf_entity_loc_num,
         (len(set(pf_entities_author)) / pf_entity_loc_num) / (
                 len(set(non_pf_entities_author)) / non_pf_entity_loc_num)])
    return len(set(pf_entities_cmt)), pf_entities_change_loc, len(set(pf_entities_author))

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


# def _format_file_path(filenames, pf_entities):
#     result = dict()
#     for pf_entity in pf_entities:
#         for file in filenames:
#             if pf_entity.replace('.', '\\') in file:
#                 result[file] = pf_entity
#                 break
#     # print(len(result))
#     return result

def _format_file_path(filenames, pf_entities):
    result = list()
    for pf_entity in pf_entities:
        for file in filenames:
            if pf_entity.replace('.', '/') in file:
                result.append([file, pf_entity])
                break
    # print(len(result))
    return result