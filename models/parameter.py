__author__ = 'danga_000'

class Parameter:
    def __init__(self, pparameterid, pcycle_id, palgoversion,pname,pmin,pmax,pchange,pdefault):
        self.parameterid = pparameterid
        self.cycle_id = pcycle_id
        self.algoversion = palgoversion
        self.name = pname
        self.min = pmin
        self.max = pmax
        self.change = pchange
        self.default = pdefault