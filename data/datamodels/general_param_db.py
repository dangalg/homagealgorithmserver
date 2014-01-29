from logic.models.general_param import General_Param

__author__ = 'danga_000'
from data import db

def get_general_params():
    gps = []
    query = "SELECT * FROM GeneralParams"
    cursor = db.get_cursor_from_query(query)
    general_params = cursor.fetchall()
    for row in general_params:
        gp = General_Param(row[0],row[1])
        gps.append(gp)
    return gps

def insert_general_param(generalparam):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO GeneralParams(param_name,
         param_val)
         VALUES ('{0}', {1})""".format(generalparam.name,generalparam.val)
    db.dml(query)

def update_general_param_val_by_name(val, name):
    # Prepare SQL query to UPDATE required records
    query = "UPDATE GeneralParams SET param_val = {0} WHERE param_name = '{1}'".format(val,name)
    db.dml(query)
