from models.generalparam import GeneralParam

__author__ = 'danga_000'
from data import db

def get_general_params():
    gps = {}
    query = "SELECT * FROM generalparams"
    cursor = db.get_cursor_from_query(query)
    general_params = cursor.fetchall()
    for row in general_params:
        gp = GeneralParam(row[0],row[1])
        gps[gp.name] = gp.val
    return gps

def get_general_param_by_name(name):
    query = 'SELECT * FROM generalparams WHERE param_name ="{0}"'.format(name)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        gp = GeneralParam(row[0],row[1])
        return gp

def insert_general_param(generalparam):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO generalparams(param_name,
         param_val)
         VALUES ('{0}', '{1}')""".format(generalparam.name,generalparam.val)
    db.dml(query)

def update_general_param_val_by_name(generalparam):
    # Prepare SQL query to UPDATE required records
    query = 'UPDATE generalparams SET param_val = "{0}" WHERE param_name = "{1}"'.format(generalparam.val,generalparam.name)
    db.dml(query)
