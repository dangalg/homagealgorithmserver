__author__ = 'danga_000'


class Parameter:
    def __init__(self,pname,pmin,pmax,pchange,pdefault):
        self.name = pname
        self.min = pmin
        self.max = pmax
        self.change = pchange
        self.default = pdefault