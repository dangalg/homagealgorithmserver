__author__ = 'danga_000'

from data.datamodels import auto_run_db

class AutoRun:
    def __init__(self,pcycleid,palgoversion,pparams,pstartdate,penddate,pavgscore):
        self.cycleid = pcycleid
        self.algoversion = palgoversion
        self.params = pparams
        self.startdate = pstartdate
        self.enddate = penddate
        self.avgscore = pavgscore


def get_AutoRun_by_cycleid(cycleid):
    return auto_run_db.get_AutoRun_by_cycleid(cycleid)

def insert_autorun(autorun):
    auto_run_db.insert_autorun(autorun)

def delete_autorun_by_cycleid(autorun):
    auto_run_db.delete_autorun_by_cycleid(autorun)