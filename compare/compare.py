import os
# from builtins import reduce
from file import fileIO
from PIL import ImageChops
import math, operator


__author__ = 'danga_000'

def run_compare_on_frame(algofile, algofolder, algoversion, gtfile, params):
    # algofile = fileIO.get_file_by_name_read(os.path.abspath(algofilepath))
    # gtfile = fileIO.get_file_by_name_read(os.path.abspath(gtfilepath))
    #Algo_Path Countour_Path First_Frame_Path -bmp Output_Path
    return calculate(algofile, gtfile, params)

def calculate(algofile, gtfile, params):
    score = 88
    return score

# # compare two images... if you need it
# def rmsdiff(im1, im2):
#     "Calculate the root-mean-square difference between two images"
#
#     h = ImageChops.difference(im1, im2).histogram()
#
#     # calculate rms
#     return math.sqrt(reduce(operator.add,
#         map(lambda h, i: h*(i**2), h, range(256))
#     ) / (float(im1.size[0]) * im1.size[1]))