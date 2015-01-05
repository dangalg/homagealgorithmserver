__author__ = 'dangalg'

from models.crash_run import CrashRun


from data import db

def get_top_cycle_id():
    query = "SELECT * FROM crashrun ORDER BY cycle_id DESC LIMIT 1"
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        crashrun = CrashRun(row[0],row[1],row[2],row[3],row[4],row[5])
        return crashrun.cycleid
    else:
        return None

def insert_crashrun(crashrun):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO crashrun (cycle_id,algo_version,params,start_date,end_date,crash_count)
         VALUES ({0},'{1}','{2}','{3}','{4}',{5})""".format(crashrun.cycleid,crashrun.algoversion,crashrun.params,crashrun.startdate,crashrun.enddate,crashrun.crashcount)
    db.dml(query)


def update_crashrun(crashrun):
    # Prepare SQL query to UPDATE required records
    query = 'UPDATE crashrun SET algo_version = "{0}", params = "{1}", start_date = "{2}", end_date = "{3}", crash_count = {4} ' \
            'WHERE cycle_id = {5}'.format(crashrun.algoversion,
                                                 crashrun.params,
                                                 crashrun.startdate,
                                                 crashrun.enddate,
                                                 crashrun.crashcount,
                                                 crashrun.cycleid)
    db.dml(query)


def get_crashrun_by_algorithem_params(crashrun):
    query = "SELECT * FROM crashrun " \
            "WHERE algo_version = '{0}' AND params = '{1}'".format(crashrun.algoversion, crashrun.params)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        autorun = CrashRun(row[0],row[1],row[2],row[3],row[4],row[5])
        return autorun