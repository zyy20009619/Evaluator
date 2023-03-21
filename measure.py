# -*- coding:utf-8 -*-
import os
import csv
import argparse
import datetime
from function_file import measure_package_metrics, compare_diff, measure_module_metrics, measure_multi_version
from detect_algo.detect_root_cause import analyse_data
from detect_algo.scan_quality_change import detect_change
from arch_debt.measure_arch import com_mc


def command():
    current_time = datetime.datetime.now()
    print("begin_time:" + str(current_time))

    parser = argparse.ArgumentParser(description='Measure architecture quality.')
    parser.add_argument('-opt', help='function options(sv/mv/com/det/cmc)',
                        default='mv')  # single version measure/multi-version measure/compare
    # for different objects
    parser.add_argument('-obj', help='object(extension/common)', default=r'common')
    parser.add_argument('-pro', help='project path', default=r'D:\paper-data-and-result\data\dataset\others\apollo')
    parser.add_argument('-ver', help='project version', default='v0.4.0?v0.5.0')
    parser.add_argument('-dep', help='dependency file path', default=r'')
    # parser.add_argument('-mp', help='mapping between module and packages', default='')
    # parser.add_argument('-pp', help='mapping between old package name and new package name', default='')
    parser.add_argument('-p1', help='the measure result path of the previous version', default=r'')
    parser.add_argument('-p2', help='the measure result path of the later version', default=r'')
    # parser.add_argument('-diff', help='the folder path of diff result', default=r'')
    parser.add_argument('-det', help='detected result files path', default=r'')
    parser.add_argument('-th', help='detected result threshold', default=r'')
    # parser.add_argument('-cause', help='causes files path', default=r'')
    parser.add_argument('-out', help='the folder path of output', default=r'D:\test')
    parser.add_argument('-lang', help='project language', default=r'java')

    args = parser.parse_args()
    opt = args.opt
    pro = args.pro
    obj = args.obj
    ver = args.ver
    dep = args.dep
    # mpmapping = args.mp
    # ppmapping = args.pp
    path1 = args.p1
    path2 = args.p2
    # diff = args.diff
    det = args.det
    th = args.th
    # cause = args.cause
    output = args.out
    lang = args.lang

    if opt == '':
        print('please input function option!!')
        return
    else:
        if opt != 'com':
            if obj == '':
                print('please input data object!!')
                return
            elif opt != 'det' and pro == '':
                print('please input project path!!')
                return
            elif opt != 'det' and ver == '':
                print('please input project version!!')
                return
        # if output == '' or not os.path.exists(output):
        #     print('Please input output path!!!')
        #     return
        if opt == 'mv' and '?' not in ver:
            print('Please split by question mark!!!')
            return
        if opt == 'com' and (path1 == '' or path2 == ''):
            print('Please input compared data path!!!')
            return
        # if opt == 'det' and diff == '':
        #     print('Please input diff data path!!!')
        #     return
        if opt == 'det' and obj == 'extension' and (path1 == '' or path2 == ''):
            print('Please input detected data path!!!')
            return

    if opt == 'sv':
        if not mpmapping:
            if len(measure_package_metrics(pro, dep, output, ver, dict(), 'sv', lang)) != 0:
                print('Measure finished!!!')
        else:
            if measure_module_metrics(pro, dep, output, mpmapping, 'sv'):
                print('Measure finished!!!')
    elif opt == 'mv':
        measure_multi_version(pro, dep, output, 'mv', ver, obj, lang)
        print('Measure multi versions finished!!!')
    # elif opt == 'com':
    #     if compare_diff(path1, path2, ppmapping, output):
    #         print('Compare finished!!!')
    #     else:
    #         print('The file path is not exist!')
    # elif opt == 'det' and opt != 'extension':
    #     if analyse_data(diff, output):
    #         print('Analyse finished!!!')
    #     else:
    #         print('The file path is not exist!')
    elif opt == 'det':
        if detect_change(path1, path2, output, opt, th):
            print('Detect finished!!!')
        else:
            print('The file path is not exist!')
    elif opt == 'cmc':
        if com_mc(pro, ver, det, output):
            print('Compete finished!!!')
        else:
            print('The file path is not exist!')

    current_time = datetime.datetime.now()
    print("end_time:" + str(current_time))


def test():
    # measure_package_metrics(r'D:\paper-data-and-result\results\c-results\main\Super-Simple-Tasker', r'D:\paper-data-and-result\results\c-results', r'D:\paper-data-and-result\results\c-results', 'main', dict(), 'c')
    # with open('./projects.txt', encoding='utf-8') as file:
    #     content = file.readlines()
    # for line in content:
    #     tmp = line.split(',')
    #     pro_path = tmp[0]
    #     pro_name = tmp[1]
    #     ver = tmp[2]
    #     com_mc(pro_path, ver, '', pro_name, 'tc')
        # measure_multi_version(pro_path, '', os.path.join(r'D:\test', pro_name), 'mv', ver, 'common', 'java')
    # # with open('./count.csv.', 'w', encoding='UTF8', newline='') as file1:
    # #     writer = csv.writer(file1)
    # #     writer.writerow(['project name', 'version', 'loc', '#files', '#commits'])
    # # 最优参数选择实验
    # base_path = r'D:\paper-data-and-result\results\c-results'
    # for line in content:
    #     tmp = line.split('\t')
    #     pro_name = tmp[0]
    #     git_url = tmp[1]
    #     project_path = os.path.join(base_path, 'projects//' + pro_name)
    #     out_path = os.path.join(base_path, 'output//' + pro_name)
    # #     os.chdir(base_path + '//projects')
    # #     os.system("git clone " + git_url)
    #     measure_package_metrics(project_path, r'D:\paper-data-and-result\results\c-results\embed-c-output-dir\embed-c-output-dir', out_path, 'main', dict(), 'c')

    #     outpath = os.path.join(base_path, pro_name)
    #     ver = tmp[2]
    #     vers = ver.split('?')
    #     # os.chdir(project_path)
    #     # os.system("git checkout -f " + ver)
    #
    #     measure_multi_version(project_path, outpath, outpath, 'mv', vers, 'common')
    # compare_diff(r'D:\paper-data-and-result\results\android-results\实验结果\honor-out\r', r'D:\paper-data-and-result\results\android-results\实验结果\aosp-out\base\android-11.0.0_r35', '', r'D:\paper-data-and-result\results\android-results\实验结果\honor-out')
    # analyse_data(r'D:\paper-data-and-result\results\android-results\实验结果\honor-out\diffResult(r2android11)', r'D:\paper-data-and-result\results\android-results\实验结果\honor-out', 'honor')
    detect_change(r'D:\paper-data-and-result\results\bishe-results\android-result\honor\s\android-12.0.0_r2',
                  r'D:\paper-data-and-result\results\bishe-results\android-result\honor\s', 'extension', 0.6)
    # detect_change(r'D:\paper-data-and-result\results\bishe-results\mc-result\apollo\v0.4.0', r'D:\paper-data-and-result\results\bishe-results\mc-result\apollo\v0.5.0', 'common', 0.6)
    # detect_change(vers[0].replace('\n', ''), vers[1].replace('\n', ''), 'extension', 0.6)
    # analyse_data(r'D:\paper-data-and-result\results\paper-results\mv\apollo-enre-out\diffResult', r'D:\paper-data-and-result\results\paper-results\mv\apollo-enre-out', 'common')
    # com_mc(project_path, vers[2:], os.path.join(outpath, 'analyseResult' + str(1)))

    # 统计代码行和文件数
    # loc_count = os.popen('cloc .').read()
    # tmp_loc = loc_count.split('\n')
    # tmp_loc1 = tmp_loc[len(tmp_loc) - 3].split(' ')
    # loc = tmp_loc1[len(tmp_loc1) - 1]
    # file = tmp_loc1[len(tmp_loc1) - 1]
    # 统计commit
    # log = subprocess.Popen('git log --numstat --date=iso', shell=True, stdout=subprocess.PIPE,
    #                        stderr=subprocess.STDOUT)
    # log_out = log.communicate()[0].decode().split('\n')
    # commit_num = 0
    # for log_len in log_out:
    #     if "commit" in str(log_len):
    #         commit_num = commit_num + 1
    #
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # writer.writerow([pro_name, ver, 'loc', 'file', commit_num])


if __name__ == '__main__':
    test()
