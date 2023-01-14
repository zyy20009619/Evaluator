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
                        default='com')  # single version measure/multi-version measure/compare
    parser.add_argument('-pro', help='project path', default=r'G:\数据集\MicroServices\projects\apollo')
    parser.add_argument('-obj', help='object(aosp/others)', default=r'')
    parser.add_argument('-ver', help='project version', default='v0.6.0?0.6.2?v0.6.3?v0.7.0?v0.8.0?v0.9.0?v0.9.1?v0.10.0?v0.10.1?v0.10.2?v0.11.0?v1.0.0?v1.1.0?v1.1.1?v1.1.2?v1.2.0?v1.3.0?v1.4.0?v1.5.0?v1.5.1?v1.6.0?v1.6.1?v1.6.2?v1.7.0?v1.7.1?v1.7.2?v1.8.0?v1.8.1?v1.8.2?v1.9.0?v1.9.1?v1.9.2?v2.0.0-RC1?v2.0.0?v2.0.1')
    parser.add_argument('-dep', help='dependency file path', default=r'')
    parser.add_argument('-mp', help='mapping between module and packages', default='')
    parser.add_argument('-pp', help='mapping between old package name and new package name', default='')
    parser.add_argument('-c1', help='the measure result path of the previous version', default=r'')
    parser.add_argument('-c2', help='the measure result path of the later version', default=r'')
    parser.add_argument('-diff', help='the folder path of diff result', default=r'G:\实验结果\microservice\apollo-out\diffResult')
    parser.add_argument('-det', help='detected files path', default=r'')
    parser.add_argument('-cause', help='causes files path', default=r'')
    parser.add_argument('-out', help='the folder path of output', default=r'G:\实验结果\microservice\apollo-out')

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
    # if (opt != 'com' or opt != 'det') and pro == '':
    #     print('please input project path!!')
    #     return
    # if (opt != 'com' or opt != 'det') and dep == '':
    #     print('please input dep path!!')
    #     return
    # if (opt != 'com' or opt != 'det') and not os.path.exists(dep):
    #     print('The file path is not exist, please input correct path!!!')
    #     return
    if output == '' or not os.path.exists(output):
        print('Please input output path!!!')
        return
    # if (opt != 'com' or opt != 'det') and ver == '':
    #     print('Please input version!!!')
    #     return
    if opt == 'mv' and '?' not in ver:
        print('Please split by question mark!!!')
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
            measure_multi_version(pro, dep, output, 'mv', ver)
            print('Measure multi versions finished!!!')
    elif opt == 'cmc':
        if com_mc(pro, ver, cause, output):
            print('Compete finished!!!')
        else:
            print('The file path is not exist!')
    else:
        if com1 and com2:
            if compare_diff(com1, com2, ppmapping, output):
                print('Compare finished!!!')
            else:
                print('The file path is not exist!')
        elif diff:
            if analyse_data(diff, output, obj):
                print('Analyse finished!!!')
            else:
                print('The file path is not exist!')
        elif det:
            if detect_change(det, output):
                print('Detect finished!!!')
            else:
                print('The file path is not exist!')

    current_time = datetime.datetime.now()
    print("end_time:" + str(current_time))


if __name__ == '__main__':
    command()