__author__ = 'danga_000'
from data import db

class General_Param:
    def __init__(self,pname,pval):
        self.name = pname
        self.val = pval



def get_general_params():
    gps = []
    query = "SELECT * FROM GeneralParams"
    cursor = db.get_cursor_from_query(query)
    general_params = cursor.fetchall()
    for row in general_params:
        gp = General_Param(row[0],row[1])
        gps.append(gp)
    return gps
