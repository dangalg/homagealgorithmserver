from data.data_services import general_param_db

__author__ = 'danga_000'


def get_general_params():
    return general_param_db.get_general_params()

def insert_general_param(generalparam):
    general_param_db.insert_general_param(generalparam)

def update_general_param_val_by_name(name, val):
    general_param_db.update_general_param_val_by_name(name,val)