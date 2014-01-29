from data import db

__author__ = 'danga_000'


class Parameter:
    def __init__(self,pname,pmin,pmax,pchange,pdefault):
        self.name = pname
        self.min = pmin
        self.max = pmax
        self.change = pchange
        self.default = pdefault

def get_param_by_name(name):
    query = "SELECT * FROM Parameters WHERE param_name = '{0}'".format(name)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    parameter = Parameter(row[0],row[1],row[2],row[3],row[4])
    return parameter

def insert_param(parameter):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO Parameters(param_name,
         param_min, param_max, param_change, param_default)
         VALUES ('{0}', {1}, {2}, {3}, {4})""".format(parameter.name,parameter.min,parameter.max,parameter.change,parameter.default)
    db.dml(query)

def update_param_by_name(name,parameter):
    # Prepare SQL query to UPDATE required records
    query = "UPDATE Parameters SET param_min = {0}, param_max = {1},param_change = {2},param_default = {3}  " \
            "WHERE param_name = '{4}'".format(parameter.min,parameter.max,parameter.change,parameter.default,name)
    db.dml(query)

def delete_param_by_name(name):
    # Prepare SQL query to UPDATE required records
    query = "DELETE FROM Parameter WHERE param_name = '{0}'".format(name)
    db.dml(query)