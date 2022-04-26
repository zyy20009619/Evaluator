import argparse
import sys
import os
from function_file import measure_package_metrics, compare_diff, measure_module_metrics


def command():
    parser = argparse.ArgumentParser(description='Measure architecture quality.')
    parser.add_argument('-d', '--dep', help='dependency file path')
    parser.add_argument('-mp', '--mpmapping', help='mapping between module and packages')
    parser.add_argument('-pp', '--ppmapping', help='mapping between old package name and new package name')
    parser.add_argument('-c1', '--con1', help='the measure result path of the previous version')
    parser.add_argument('-c2', '--con2', help='the measure result path of the later version')

    args = parser.parse_args()
    dep = args.dep
    mpmapping = args.mpmapping
    ppmapping = args.ppmapping
    con1 = args.con1
    con2 = args.con2
    if dep and not mpmapping:
        if measure_package_metrics(dep):
            print('Measure finished!!!')
        else:
            print('The file path is not exist!')
    if dep and mpmapping:
        if measure_module_metrics(dep, mpmapping):
            print('Measure finished!!!')
        else:
            print('The file path is not exist!')
    if con1 and con2:
        if compare_diff(con1, con2, ppmapping):
            print('Compare finished!!!')
        else:
            print('The file path is not exist!')


if __name__ == '__main__':
    # print(os.getcwd())
    # print(sys.path)
    # sys.path.append(os.getcwd())
    command()