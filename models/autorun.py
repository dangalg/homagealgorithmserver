import datetime

__author__ = 'danga_000'

class AutoRun:

    def __init__(self,pcycleid,palgoversion,pparams,pstartdate,penddate,pavgscore,pcrashcount):
        self.cycleid = pcycleid
        self.algoversion = palgoversion
        self.params = pparams
        self.startdate = pstartdate
        self.enddate = penddate
        self.avgscore = pavgscore
        self.crashcount = pcrashcount