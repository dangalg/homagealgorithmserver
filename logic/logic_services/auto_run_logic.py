__author__ = 'danga_000'

from data.data_services import auto_run_db

def get_new_cycle_id():
    topcycleid = auto_run_db.get_top_cycle_id()
    cycleid = 1
    if topcycleid:
        cycleid = topcycleid + 1
    return cycleid

def get_autorun_by_cycleid_algorithem_params(autorun):
    return auto_run_db.get_autorun_by_cycleid_algorithem_params(autorun)

def insert_update_autorun(autorun):
    if get_autorun_by_cycleid_algorithem_params(autorun):
        auto_run_db.update_autorun(autorun)
    else:
        auto_run_db.insert_autorun(autorun)

def delete_autorun_by_cycleid(autorun):
    auto_run_db.delete_autorun_by_cycleid(autorun)