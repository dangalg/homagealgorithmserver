import os
import subprocess
from data.aws_helper import uploadfiletos3
from file.fileIO import get_plf_file

from utils.log import log_information
from utils import consts
from subprocess import Popen, PIPE

__author__ = 'danga_000'


def create_algorithm_output_path(gps, cycleid, video):
    # Create the path to save the frame
    path = ''
    if gps[consts.crashrunname].val:
        path = os.path.abspath(gps[consts.crashoutputfoldername].val + gps[consts.algoversionname].val + "/" + str(cycleid)
            + "/" + video.videoname + "/")
    else:
        path = os.path.abspath(gps[consts.outputfoldername].val + gps[consts.algoversionname].val + "/" + str(cycleid)
            + "/" + video.videoname + "/")
    # path = os.path.abspath(video.path + "/" + algoversion + "/"  + str(cycleid) + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def create_params_output_path(gps,cycleid):
    # Create the path to save the frame
    path = ''
    if gps[consts.crashrunname].val:
        path = os.path.abspath(gps[consts.crashoutputfoldername].val + gps[consts.algoversionname].val + "/"+ str(cycleid) + "/")
    else:
        path = os.path.abspath(gps[consts.outputfoldername].val + gps[consts.algoversionname].val + "/"+ str(cycleid) + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    return path  + '/' + consts.paramsxml

def run_algorithm(gps, cycleid, video):
    algoplfpath = create_algorithm_output_path(gps, cycleid, video)
    paramspath = create_params_output_path(gps,cycleid)
    # UniformMattingCA.exe -CA params.xml contour.ctr image-0001.jpg -avic -r25 -mp4 output.avi
    algocommand = gps[consts.algofoldername].val + gps[consts.algoversionname].val + '/' +  'UniformMattingCA.exe -CA ' \
    + paramspath + ' ' \
    + video.path + '/' + video.videoname + '.ctr ' \
    + ' ' + video.path + '/' + 'Frames' + '/image-0001.jpg -avic -r25 -mp4 ' \
    + algoplfpath + '/' + 'output.avi'
    # os.system(algocommand)

    awsoutputpath = 'Output/' + gps[consts.algoversionname].val + "/" + str(cycleid) + "/" + video.videoname + '/' + 'output.avi'
    try:
        print("Start Algorithem")


        cmd = algocommand
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        print("message: " + str(stdout))
        print("error: " + str(stderr))
        result = "good"
        if "failed" in str(stderr):
            result = str(stderr)
        if not gps[consts.crashrunname].val:
            print("Upload to aws")
            uploadfiletos3('homage-automation', awsoutputpath, algoplfpath + '/' + 'output.avi')
    except OSError as e:
        log_information(gps, str(e.args).replace("'",""))

    outputplf = get_plf_file(algoplfpath)
    if outputplf:
        return algoplfpath + '/' + outputplf, awsoutputpath, result
    return None, awsoutputpath, result
