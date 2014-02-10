__author__ = 'danga_000'

from data.data_services import auto_run_db

def get_top_cycle_id():
    return auto_run_db.get_top_cycle_id()

def get_autoRun_by_cycleid(cycleid):
    return auto_run_db.get_AutoRun_by_cycleid(cycleid)

def insert_autorun(autorun):
    auto_run_db.insert_autorun(autorun)

def delete_autorun_by_cycleid(autorun):
    auto_run_db.delete_autorun_by_cycleid(autorun)