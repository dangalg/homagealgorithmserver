__author__ = 'danga_000'

class Parameter:
    def __init__(self,pcycleid,palgoversion,pname,pmin,pmax,pchange,pdefault):
        self.cycleid = pcycleid
        self.algoversion = palgoversion
        self.name = pname
        self.min = pmin
        self.max = pmax
        self.change = pchange
        self.default = pdefault