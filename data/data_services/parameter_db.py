from data import db
from models.parameter import Parameter

__author__ = 'danga_000'

def get_all_params():
    parameters = []
    query = "SELECT * FROM Parameters"
    cursor = db.get_cursor_from_query(query)
    params = cursor.fetchall()
    for row in params:
        param = Parameter(row[0],row[1],row[2],row[3],row[4],row[5])
        parameters.append(param)
    return parameters

def get_params_by_algo_version(version):
    parameters = []
    query = """SELECT * FROM Parameters WHERE algo_version = '{0}'""".format(version)
    cursor = db.get_cursor_from_query(query)
    params = cursor.fetchall()
    for row in params:
        param = Parameter(row[0],row[1],row[2],row[3],row[4],row[5])
        parameters.append(param)
    return parameters

def get_param_by_name(version, name):
    query = "SELECT * FROM Parameters WHERE algo_version = '{0}' AND param_name = '{1}'".format(version, name)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        parameter = Parameter(row[0],row[1],row[2],row[3],row[4],row[5])
        return parameter

def insert_param(version, parameter):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO Parameters(algo_version,param_name,
         param_min, param_max, param_change, param_default)
         VALUES ('{0}', '{1}', {2}, {3}, {4},{5})""".format(version, parameter.name,parameter.min,parameter.max,parameter.change,parameter.default)
    db.dml(query)

def update_param_by_name(version,name,parameter):
    # Prepare SQL query to UPDATE required records
    query = "UPDATE Parameters SET param_min = {0}, param_max = {1},param_change = {2},param_default = {3}  " \
            "WHERE algo_version = '{4}' AND param_name = '{5}'".format(parameter.min,parameter.max,parameter.change,parameter.default,version,name)
    db.dml(query)

def delete_param_by_name(version, name):
    # Prepare SQL query to UPDATE required records
    query = "DELETE FROM Parameters WHERE algo_version = '{0}' AND param_name = '{1}'".format(version, name)
    db.dml(query)

