from logic.models.auto_run import AutoRun

__author__ = 'danga_000'

from data import db


def get_AutoRun_by_cycleid(cycleid):
    query = "SELECT * FROM AutoRun " \
            "WHERE cycle_id = {0}".format(cycleid)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    autorun = AutoRun(row[0],row[1],row[2],row[3],row[4],row[5])
    return autorun


def insert_autorun(autorun):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO AutoRun(cycle_id,
         algo_version, params, start_date,end_date,avg_score)
         VALUES ({0}, {1}, '{2}', '{3}','{4}',{5})""".format(autorun.cycleid,
                                                 autorun.algoversion,
                                                 autorun.params,
                                                 autorun.startdate,
                                                 autorun.enddate,
                                                 autorun.avgscore)
    db.dml(query)

def delete_autorun_by_cycleid(autorun):
    # Prepare SQL query to UPDATE required records
    query = "DELETE FROM AutoRunVideo WHERE cycle_id = {0}".format(autorun.cycleid)
    db.dml(query)