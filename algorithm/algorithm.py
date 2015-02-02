import os
import subprocess
from data import aws_helper
from data.aws_helper import uploadfiletos3
from file import zippy
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

    # Create algorithm command
    algocommand = gps[consts.algofoldername].val + gps[consts.algoversionname].val + '/' + consts.algorithmfile + ' -CA ' \
    + paramspath + ' ' \
    + video.path + '/' + video.videoname + '.ctr ' \
    + ' ' + video.path + '/' + 'Frames' + '/image-0001.jpg -avic -r25 -mp4 ' \
    + algoplfpath + '/' + 'output.avi'

    result = "good"
    s3_output_url = None
    try:
        print("Start Algorithem")

        # Run Algorithm
        cmd = algocommand
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        print("message: " + str(stdout))
        print("error: " + str(stderr))

        if "failed" in str(stderr):
            result = str(stderr)

        if not gps[consts.crashrunname].val:
            if os.path.exists(algoplfpath + '/' + 'output.avi'):
                print("Convert and Upload to aws")
                # convert avi to mp4 with ffmpeg
                cmd = 'ffmpeg -i ' + algoplfpath + '/' + 'output.avi' + ' -vcodec libx264 -b:v 1200k -y ' + algoplfpath + '/' + 'output.mp4'
                p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                stdout, stderr = p.communicate()
                print("message: " + str(stdout))
                print("error: " + str(stderr))
                # delete avi file
                os.remove(algoplfpath + '/' + 'output.avi')

    except OSError as e:
        log_information(gps, str(e.args).replace("'",""))

    outputplf = get_plf_file(algoplfpath)

    if outputplf and not gps[consts.crashrunname].val:
        return algoplfpath + '/' + outputplf, result, s3_output_url

    return None, result, s3_output_url
