from models.autorun import AutoRun

__author__ = 'danga_000'

from data import db


def get_top_cycle_id():
    query = "SELECT * FROM AutoRun ORDER BY cycle_id DESC LIMIT 1"
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        autorun = AutoRun(row[0],row[1],row[2],row[3],row[4],row[5])
        return autorun.cycleid

def get_last_algorithm_version():
    query = "SELECT * FROM AutoRun ORDER BY algo_version DESC LIMIT 1"
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        autorun = AutoRun(row[0],row[1],row[2],row[3],row[4],row[5])
        return autorun.cycleid

def get_autorun_by_cycleid_algorithem_params(autorun):
    query = "SELECT * FROM AutoRun " \
            "WHERE cycle_id = {0} AND algo_version = '{1}' AND params = '{2}'".format(autorun.cycleid, autorun.algoversion, autorun.params)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        autorun = AutoRun(row[0],row[1],row[2],row[3],row[4],row[5])
        return autorun


def insert_autorun(autorun):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO AutoRun(cycle_id,
         algo_version, params, start_date,end_date,avg_score)
         VALUES ({0}, '{1}', '{2}', '{3}','{4}',{5})""".format(autorun.cycleid,
                                                 autorun.algoversion,
                                                 autorun.params,
                                                 autorun.startdate,
                                                 autorun.enddate,
                                                 autorun.avgscore)
    db.dml(query)

def update_autorun(autorun):
    # Prepare SQL query to UPDATE required records
    query = 'UPDATE AutoRun SET algo_version = "{0}", params = "{1}", start_date = "{2}", end_date = "{3}", avg_score = {4} ' \
            'WHERE cycle_id = {5}'.format(autorun.algoversion,
                                                 autorun.params,
                                                 autorun.startdate,
                                                 autorun.enddate,
                                                 autorun.avgscore,
                                                 autorun.cycleid)
    db.dml(query)

def delete_autorun_by_cycleid(autorun):
    # Prepare SQL query to UPDATE required records
    query = "DELETE FROM AutoRunVideo WHERE cycle_id = {0}".format(autorun.cycleid)
    db.dml(query)