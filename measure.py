# -*- coding:utf-8 -*-
import os
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
    parser.add_argument('-obj', help='object(aosp/others/honor/micro)', default=r'aosp')
    parser.add_argument('-pro', help='project path', default=r'')
    parser.add_argument('-ver', help='project version', default='')
    parser.add_argument('-dep', help='dependency file path', default=r'')
    # parser.add_argument('-mp', help='mapping between module and packages', default='')
    # parser.add_argument('-pp', help='mapping between old package name and new package name', default='')
    parser.add_argument('-c1', help='the measure result path of the previous version', default=r'')
    parser.add_argument('-c2', help='the measure result path of the later version', default=r'')
    parser.add_argument('-diff', help='the folder path of diff result', default=r'')
    parser.add_argument('-det', help='detected files path', default=r'')
    parser.add_argument('-cause', help='causes files path', default=r'')
    parser.add_argument('-out', help='the folder path of output', default=r'')

    args = parser.parse_args()
    opt = args.opt
    pro = args.pro
    obj = args.obj
    ver = args.ver
    dep = args.dep
    mpmapping = args.mp
    ppmapping = args.pp
    com1 = args.c1
    com2 = args.c2
    diff = args.diff
    det = args.det
    cause = args.cause
    output = args.out

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
        if output == '' or not os.path.exists(output):
            print('Please input output path!!!')
            return
        if opt == 'mv' and '?' not in ver:
            print('Please split by question mark!!!')
            return
        if opt == 'com' and (com1 == '' or com2 == ''):
            print('Please input compared data path!!!')
            return
        if opt == 'det' and diff == '':
            print('Please input diff data path!!!')
            return

    if opt == 'sv':
        if not mpmapping:
            if len(measure_package_metrics(pro, dep, output, ver, dict(), 'sv')) != 0:
                print('Measure finished!!!')
        else:
            if measure_module_metrics(pro, dep, output, mpmapping, 'sv'):
                print('Measure finished!!!')
    elif opt == 'mv':
        if not mpmapping:
            measure_multi_version(pro, dep, output, 'mv', ver, obj)
            print('Measure multi versions finished!!!')
    elif opt == 'com':
        if compare_diff(com1, com2, ppmapping, output):
            print('Compare finished!!!')
        else:
            print('The file path is not exist!')
    elif opt == 'det':
        if analyse_data(diff, output, obj):
            print('Analyse finished!!!')
        else:
            print('The file path is not exist!')
    elif opt == 'cmc':
        if com_mc(pro, ver, cause, output):
            print('Compete finished!!!')
        else:
            print('The file path is not exist!')
    #     elif det:
    #         if detect_change(det, output):
    #             print('Detect finished!!!')
    #         else:
    #             print('The file path is not exist!')

    current_time = datetime.datetime.now()
    print("end_time:" + str(current_time))


def test():
    # measure_multi_version(r'D:\paper-data-and-result\data\dataset\AOSP\projects\Android\base'.split('?'), ''.split('?'), r'D:\paper-data-and-result\results\android-results\实验结果\aosp-out\base', 'mv', 'android-11.0.0_r35?android-12.0.0_r10'.split('?'), 'aosp')
    # compare_diff(r'D:\paper-data-and-result\results\android-results\实验结果\honor-out\s', r'D:\paper-data-and-result\results\android-results\实验结果\honor-out\t', '', r'D:\paper-data-and-result\results\android-results\实验结果\honor-out')
    analyse_data(r'D:\paper-data-and-result\results\android-results\实验结果\honor-out\diffResult(s2t)', r'D:\paper-data-and-result\results\android-results\实验结果\honor-out', 'aosp')


if __name__ == '__main__':
    test()

