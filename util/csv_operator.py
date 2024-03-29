import os
import csv
from .metrics import *
import pandas as pd


def read_csv(file_path, file_name):
    res = list()
    with open(os.path.join(file_path, file_name)) as f:
        reader = csv.reader(f)
        for row in reader:
            res.append(row)
    return res


def read_csv_to_pd(file_path):
    return pd.read_csv(file_path)


def read_csv_folder(class1, class2, method1, method2):
    class1_res = read_csv_to_pd(class1)
    class2_res = read_csv_to_pd(class2)
    method1_res = read_csv_to_pd(method1)
    method2_res = read_csv_to_pd(method2)
    return class1_res, class2_res, method1_res, method2_res


def write_to_csv(result_list, file_path):
    with open(file_path, "w", newline="", encoding='utf-8') as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerows(result_list)


def write_to_one_line(result_list, file_path):
    with open(file_path, "w", newline="", encoding='utf-8') as fp:
        writer = csv.writer(fp, delimiter=",")
        for res in result_list:
            writer.writerow(res)


def write_result_to_csv(class_file_path, method_file_path, ver, content):
    class_f = open(class_file_path, 'w', encoding='utf-8', newline='')
    class_csv_writer = csv.writer(class_f)
    class_header = list()
    class_header.extend(PROJECT_METRICS)
    class_header.append("module_name")
    class_header.extend(MODULE_METRICS)
    class_header.append("class_name")
    class_header.append("filepath")
    class_header.extend(CLASS_METRICS)
    class_csv_writer.writerow(class_header)

    method_f = open(method_file_path, 'w', encoding='utf-8', newline='')
    method_csv_writer = csv.writer(method_f)
    method_header = list()
    method_header.extend(["module_name", "class_name", "filepath", "method_name"])
    method_header.extend(METHOD_METRICS)
    method_csv_writer.writerow(method_header)

    from operator import itemgetter
    project_value = list(itemgetter(*PROJECT_METRICS)(content[ver]))
    modules = content[ver]['modules']
    for module in modules:
        module_value = list(itemgetter(*MODULE_METRICS)(modules[module]))
        classes = modules[module]['classes']
        for class_name in classes:
            class_value = list(itemgetter(*CLASS_METRICS)(classes[class_name]))
            class_res = list()
            class_res.extend(project_value)
            class_res.append(module)
            class_res.extend(module_value)
            class_res.append(class_name)
            class_res.append(classes[class_name]['filepath'])
            class_res.extend(class_value)
            class_csv_writer.writerow(class_res)
            methods = classes[class_name]['methods']
            for method_name in methods:
                method_value = list(itemgetter(*METHOD_METRICS)(methods[method_name]))
                method_res = list()
                method_res.extend([module, class_name, classes[class_name]['filepath'], method_name])
                method_res.extend(method_value)
                method_csv_writer.writerow(method_res)
    class_f.close()
    method_f.close()