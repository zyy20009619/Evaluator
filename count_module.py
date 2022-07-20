import json
import csv
import argparse


def count(file_path):
    json_dic = read_file(file_path)
    f = open('result.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow([str(len(json_dic))])
    for module_name in json_dic:
        csv_writer.writerow([module_name])


def read_file(file_path):
    try:
        with open(file_path, 'r') as f:
            json_dict = json.load(f)
    except (FileExistsError, FileNotFoundError, PermissionError):
        json_dict = dict()
    return json_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Count module.')
    parser.add_argument('-m', '--measure', help='measure result file path')
    args = parser.parse_args()
    measure = args.measure

    count(measure)
