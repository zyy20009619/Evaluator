from module_measurement.project import Project


def com_metrics(version, file_contain, file_dep_matrix, struct_dep_matrix, function_dep):
    project_info = {'version': 'v1',
                    'contain': {0: {2: [6, 7, 8], 3: [9, 10, 11]}, 1: {4: [12, 13, 14], 5: [15, 16, 17]}},
                    'dep': {'module': {0: {1: 1}}, 'class': {2: {4: 1}}, 'method': {10: {14: 1}}}}
    project = Project(project_info)
    print(project)
