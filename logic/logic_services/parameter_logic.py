from data.data_services import parameter_db

__author__ = 'danga_000'

# def get_all_params():
#     return parameter_db.get_all_params()

# def get_param_by_name(cycleid, version, name):
#     return parameter_db.get_param_by_name(version, name)

def insert_param(parameter):
    parameter_db.insert_param(parameter)

# def get_params_by_algo_version(version):
#     return parameter_db.get_params_by_algo_version(version)

# def update_param_by_name(cycleid, version, name, parameter):
#     parameter_db.update_param_by_name(cycleid, version, name, parameter)

# def insert_update_param_by_name(cycleid, version, name, parameter):
#     p = get_param_by_name(cycleid, version, name)
#     if p:
#         update_param_by_name(cycleid, version, name,parameter)
#     else:
#         insert_param(cycleid, version, parameter)

# def delete_param_by_name(version, name):
#     parameter_db.delete_param_by_name(version, name)