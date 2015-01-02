import os
import subprocess
from data.aws_helper import uploadfiletos3
from file import fileIO
from file.fileIO import list_frames_by_path, get_plf_file
from logic.logic_services import general_param_logic
from utils import log
from utils.log import log_information
from utils import consts

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

def run_algorithm(gps, cycleid, video, params):
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
        result = subprocess.call(algocommand, stderr=subprocess.STDOUT, shell=True)
        log_information(gps, str(result))
        print(str(result))
        if not gps[consts.crashrunname].val:
            print("Upload to aws")
            uploadfiletos3('homage-automation', awsoutputpath, algoplfpath + '/' + 'output.avi')
    except OSError as e:
        log_information(gps, str(e.args).replace("'",""))

    outputplf = get_plf_file(algoplfpath)
    if outputplf:
        return algoplfpath + '/' + outputplf, awsoutputpath
    return None, awsoutputpath
