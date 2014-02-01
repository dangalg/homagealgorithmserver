from data.datamodels import parameter_db

__author__ = 'danga_000'


class Parameter:
    def __init__(self,pname,pmin,pmax,pchange,pdefault):
        self.name = pname
        self.min = pmin
        self.max = pmax
        self.change = pchange
        self.default = pdefault

def get_param_by_name(name):
    return parameter_db.get_param_by_name(name)

def insert_param(parameter):
    parameter_db.insert_param(parameter)

def update_param_by_name(name,parameter):
    parameter_db.update_param_by_name(name,parameter)

def delete_param_by_name(name):
    parameter_db.delete_param_by_name(name)