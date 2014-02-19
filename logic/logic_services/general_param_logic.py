from data.data_services import general_param_db

__author__ = 'danga_000'


def get_general_params():
    return general_param_db.get_general_params()

def get_general_param_by_name(name):
    return general_param_db.get_general_param_by_name(name)

def insert_update_general_param(generalparam):
    if get_general_param_by_name(generalparam.name):
        general_param_db.update_general_param_val_by_name(generalparam)
    else:
        general_param_db.insert_general_param(generalparam)