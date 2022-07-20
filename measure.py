import os
import argparse
from function_file import measure_package_metrics, compare_diff, measure_module_metrics, measure_multi_version
from detect_algo.detect_root_cause import analyse_data


def command():
    parser = argparse.ArgumentParser(description='Measure architecture quality.')
    parser.add_argument('-opt', help='function options', default='')  # single version measure/multi-version measure/compare
    parser.add_argument('-dep', help='dependency file path', default='')
    parser.add_argument('-mp', help='mapping between module and packages', default='')
    parser.add_argument('-pp', help='mapping between old package name and new package name', default='')
    parser.add_argument('-c1', help='the measure result path of the previous version', default='')
    parser.add_argument('-c2', help='the measure result path of the later version', default='')
    parser.add_argument('-diff', help='the folder path of diff result', default='')
    parser.add_argument('-out', help='the folder path of output', default='')

    # parser.add_argument('-opt', '--option', help='function options')  # single version measure/multi-version measure/compare
    # parser.add_argument('-d', '--dep', help='dependency file path')
    # parser.add_argument('-mp', '--mpmapping', help='mapping between module and packages')
    # parser.add_argument('-pp', '--ppmapping', help='mapping between old package name and new package name')
    # parser.add_argument('-c1', '--com1', help='the measure result path of the previous version')
    # parser.add_argument('-c2', '--com2', help='the measure result path of the later version')
    # parser.add_argument('-df', '--diff', help='the folder path of diff result')
    # parser.add_argument('-out', '--output', help='the folder path of output')

    args = parser.parse_args()
    opt = args.opt
    dep = args.dep
    mpmapping = args.mp
    ppmapping = args.pp
    com1 = args.c1
    com2 = args.c2
    diff = args.diff
    output = args.out

    if opt == '':
        print('please input function option!!')
        return
    if dep == '':
        print('please input dep path!!')
        return
    if not os.path.exists(dep):
        print('The file path is not exist, please input correct path!!!')
        return
    if output == '' or not os.path.exists(output):
        output = './result'

    if opt == 'sv':
        if not mpmapping:
            if measure_package_metrics(dep, output):
                print('Measure finished!!!')
        else:
            if measure_module_metrics(dep, output, mpmapping):
                print('Measure finished!!!')
    elif opt == 'mv':
        if not mpmapping:
            measure_multi_version(dep, output)
    else:
        if com1 and com2:
            if compare_diff(com1, com2, ppmapping, output):
                print('Compare finished!!!')
            else:
                print('The file path is not exist!')
        if diff:
            if analyse_data(diff, output):
                print('Analyse finished!!!')
            else:
                print('The file path is not exist!')


if __name__ == '__main__':
    command()