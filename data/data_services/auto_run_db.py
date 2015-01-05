from models.autorun import AutoRun

__author__ = 'danga_000'

from data import db


def get_top_cycle_id():
    query = "SELECT * FROM autorun ORDER BY cycle_id DESC LIMIT 1"
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        autorun = AutoRun(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
        return autorun.cycleid

# def get_last_algorithm_version():
#     query = "SELECT * FROM AutoRun ORDER BY algo_version DESC LIMIT 1"
#     cursor = db.get_cursor_from_query(query)
#     row = cursor.fetchone()
#     if row:
#         autorun = AutoRun(row[0],row[1],row[2],row[3],row[4],row[5])
#         return autorun.cycleid

def get_autorun_by_algorithem_params(autorun):
    query = "SELECT * FROM autorun " \
            "WHERE algo_version = '{0}' AND params = '{1}'".format(autorun.algoversion, autorun.params)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        autorun = AutoRun(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
        return autorun


def insert_autorun(autorun):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO autorun(cycle_id,
         algo_version, params, start_date,end_date,avg_score,crash_count)
         VALUES ({0}, '{1}', '{2}', '{3}','{4}',{5},{6})""".format(autorun.cycleid,
                                                 autorun.algoversion,
                                                 autorun.params,
                                                 autorun.startdate,
                                                 autorun.enddate,
                                                 autorun.avgscore,
                                                 autorun.crashcount)
    db.dml(query)

def update_autorun(autorun):
    # Prepare SQL query to UPDATE required records
    query = 'UPDATE autorun SET algo_version = "{0}", params = "{1}", start_date = "{2}", end_date = "{3}", avg_score = {4}, crash_count = {5} ' \
            'WHERE cycle_id = {6}'.format(autorun.algoversion,
                                                 autorun.params,
                                                 autorun.startdate,
                                                 autorun.enddate,
                                                 autorun.avgscore,
                                                 autorun.crashcount,
                                                 autorun.cycleid)
    db.dml(query)
#
def delete_autorun_by_cycleid(autorun):
    # Prepare SQL query to UPDATE required records
    query = "DELETE FROM autorunvideo WHERE cycle_id = {0}".format(autorun.cycleid)
    db.dml(query)