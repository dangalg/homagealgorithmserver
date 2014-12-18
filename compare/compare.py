import os
# from builtins import reduce
import subprocess
from file import fileIO
from PIL import ImageChops
import math, operator


__author__ = 'danga_000'



def run_compare_on_frame(framenum, avgdistX, avgdistY, varX, varY, pctX, pctY):
    return calculate(framenum, avgdistX, avgdistY, varX, varY, pctX, pctY)

def calculate(framenum, avgdistX, avgdistY, varX, varY, pctX, pctY):
    # Frame Grade = Min(pixel distance percentage) X 100 - Max(sqrt(Var))
    pixledistancepercentage = pctY
    if pctX < pctY:
        pixledistancepercentage = pctX

    var = varY
    if varX > varY:
        var = varX

    score = float((float(pixledistancepercentage) * float(100.00)) - (float(var)))
    return float(score)