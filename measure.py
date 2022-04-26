import argparse
from function_file import measure_package_metrics, compare_diff, measure_module_metrics
from detect_algo.detect_root_cause import analyse_data


def command():
    parser = argparse.ArgumentParser(description='Measure architecture quality.')
    parser.add_argument('-d', '--dep', help='dependency file path')
    parser.add_argument('-mp', '--mpmapping', help='mapping between module and packages')
    parser.add_argument('-pp', '--ppmapping', help='mapping between old package name and new package name')
    parser.add_argument('-c1', '--com1', help='the measure result path of the previous version')
    parser.add_argument('-c2', '--com2', help='the measure result path of the later version')
    parser.add_argument('-df', '--diff', help='the folder path of diff result')
    parser.add_argument('-pro', '--project', help='the folder path of project')
    parser.add_argument('-out', '--output', help='the folder path of output')

    args = parser.parse_args()
    dep = args.dep
    mpmapping = args.mpmapping
    ppmapping = args.ppmapping
    com1 = args.com1
    com2 = args.com2
    diff = args.diff
    project = args.project
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
    if com1 and com2:
        if compare_diff(com1, com2, ppmapping):
            print('Compare finished!!!')
        else:
            print('The file path is not exist!')
    if diff and project:
        if analyse_data(diff, project):
            print('Analyse finished!!!')
        else:
            print('The file path is not exist!')


if __name__ == '__main__':
    # print(os.getcwd())
    # print(sys.path)
    # sys.path.append(os.getcwd())
    command()