# coding=gbk
import os
import sys
import argparse
import datetime
from function_file import measure_package_metrics, compare_diff, measure_module_metrics, measure_multi_version
from detect_algo.detect_root_cause import analyse_data


def command():
    current_time = datetime.datetime.now()
    print("begin_time:" + str(current_time))

    parser = argparse.ArgumentParser(description='Measure architecture quality.')
<<<<<<< HEAD
    parser.add_argument('-opt', help='function options(sv/mv/com)', default='mv')  # single version measure/multi-version measure/compare
    parser.add_argument('-pro', help='project path', default=r'F:\research\�����չ���\ʵ��\���ݼ�\MicroServices\projects\apollo')
    parser.add_argument('-ver', help='project version', default='v0.4.0?v0.5.0')
    parser.add_argument('-dep', help='dependency file path', default=r'F:\research\�����չ���\ʵ��\ʵ����\Apollo')
=======
    parser.add_argument('-opt', help='function options(sv/mv/com)', default='com')  # single version measure/multi-version measure/compare
    parser.add_argument('-pro', help='project path', default=r'D:\毕设进展相关\实验\数据集\AOSP\projects\Android\base')
    parser.add_argument('-ver', help='project version', default='49d8b986dddd441df741698541788c5f3a9c465f?ad31dbbdcd76091d7d2d1fc6c863ee17c3bfe87d')
    parser.add_argument('-dep', help='dependency file path', default=r'D:\毕设进展相关\实验\实验结果\aosp-out\base')
>>>>>>> a2630a02a4915361f3518d56c1788e06985d0b13
    parser.add_argument('-mp', help='mapping between module and packages', default='')
    parser.add_argument('-pp', help='mapping between old package name and new package name', default='')
    parser.add_argument('-c1', help='the measure result path of the previous version', default=r'')
    parser.add_argument('-c2', help='the measure result path of the later version', default=r'')
<<<<<<< HEAD
    parser.add_argument('-diff', help='the folder path of diff result', default=r'')
    parser.add_argument('-out', help='the folder path of output', default=r'F:\research\�����չ���\ʵ��\ʵ����\Apollo')
=======
    parser.add_argument('-diff', help='the folder path of diff result', default=r'D:\毕设进展相关\实验\实验结果\lineage-out\lineage-18.1\diffResult')
    parser.add_argument('-out', help='the folder path of output', default=r'D:\毕设进展相关\实验\实验结果\lineage-out\lineage-18.1')
>>>>>>> a2630a02a4915361f3518d56c1788e06985d0b13

    args = parser.parse_args()
    opt = args.opt
    pro = args.pro
    ver = args.ver
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
    if opt != 'com' and pro == '':
        print('please input project path!!')
        return
    if opt != 'com' and dep == '':
        print('please input dep path!!')
        return
    if opt != 'com' and not os.path.exists(dep):
        print('The file path is not exist, please input correct path!!!')
        return
    if output == '' or not os.path.exists(output):
        print('Please input output path!!!')
        return
    if opt != 'com' and ver == '':
        print('Please input version!!!')
        return
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
    else:
        if com1 and com2:
            if compare_diff(com1, com2, ppmapping, output):
                print('Compare finished!!!')
            else:
                print('The file path is not exist!')
        if diff:
<<<<<<< HEAD
=======
            #TODO:暂时写死，之后计算top10加到度量过程中(或者用户可根据需求选择查看本身质量比较差的topX在新版本上有没有变得更差以及原因||用户可选择正常演化过程中演化趋势最差的topX)
            # top_10 = ['android.app', 'android.os', 'android.content', 'android.view', 'android.util', 'com.android.server', 'com.android.systemui.statusbar.phone', 'com.android.server.wm', 'android.content.pm', 'android.widget']
>>>>>>> a2630a02a4915361f3518d56c1788e06985d0b13
            if analyse_data(diff, output):
                print('Analyse finished!!!')
            else:
                print('The file path is not exist!')

<<<<<<< HEAD

def app_path():
    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)  # ʹ��pyinstaller������exeĿ¼
    return os.path.dirname(__file__)  # û���ǰ��pyĿ¼
=======
    current_time = datetime.datetime.now()
    print("end_time:" + str(current_time))
>>>>>>> a2630a02a4915361f3518d56c1788e06985d0b13


if __name__ == '__main__':
    # app_path()
    command()