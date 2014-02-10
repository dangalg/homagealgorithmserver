from data.data_services import parameter_db

__author__ = 'danga_000'

def get_all_params():
    return parameter_db.get_all_params()

def get_param_by_name(name):
    return parameter_db.get_param_by_name(name)

def insert_param(parameter):
    parameter_db.insert_param(parameter)

def update_param_by_name(name,parameter):
    parameter_db.update_param_by_name(name,parameter)

def delete_param_by_name(name):
    parameter_db.delete_param_by_name(name)