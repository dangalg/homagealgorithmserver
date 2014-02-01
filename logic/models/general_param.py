from data.datamodels import general_param_db

__author__ = 'danga_000'


class General_Param:
    def __init__(self,pname,pval):
        self.name = pname
        self.val = pval


def get_general_params():
    return general_param_db.get_general_params()

def insert_general_param(generalparam):
    general_param_db.insert_general_param(generalparam)

def update_general_param_val_by_name(val, name):
    general_param_db.update_general_param_val_by_name(val,name)