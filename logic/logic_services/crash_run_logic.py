__author__ = 'dangalg'

from data.data_services import crash_run_db

def insert_crashrun(crashrun):
        crash_run_db.insert_crashrun(crashrun)

def update_crashrun(crashrun):
        crash_run_db.update_crashrun(crashrun)

def get_new_cycle_id():
    topcycleid = crash_run_db.get_top_cycle_id()
    cycleid = 1
    if topcycleid:
        cycleid = topcycleid + 1
    return cycleid

def get_crashrun_by_algorithem_params(crashrun):
    return crash_run_db.get_crashrun_by_algorithem_params(crashrun)