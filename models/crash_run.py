__author__ = 'dangalg'

class CrashRun:
    def __init__(self,pcycleid,palgoversion,pparams,pstartdate,penddate,pcrashcount):
        self.cycleid = pcycleid
        self.algoversion = palgoversion
        self.params = pparams
        self.startdate = pstartdate
        self.enddate = penddate
        self.crashcount = pcrashcount