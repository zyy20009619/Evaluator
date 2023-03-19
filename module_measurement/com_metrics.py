from module_measurement.project import Project


def com_metrics(version, var_id_to_var, file_contain, file_dep_matrix, struct_dep_matrix, function_dep, out_path):
    project_info = {'version': 'v1',
                    'contain': file_contain,
                    'dep': {'module': file_dep_matrix, 'class': struct_dep_matrix, 'method': function_dep}}
    project = Project(var_id_to_var, project_info, out_path)
    # print(project)
