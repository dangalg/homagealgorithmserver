import os
import subprocess
from file import fileIO
from file.fileIO import list_frames_by_path, get_plf_file
from logic.logic_services import general_param_logic
from utils import log
from utils.log import log_information
from utils import consts

__author__ = 'danga_000'


def create_algorithm_output_path(gps, cycleid, video):
    # Create the path to save the frame
    path = os.path.abspath(gps[consts.outputfolder].val + gps[consts.algoversion].val + "/" + str(cycleid)
        + "/" + video.videoname + "/")
    # path = os.path.abspath(video.path + "/" + algoversion + "/"  + str(cycleid) + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def create_params_output_path(gps, cycleid):
    # Create the path to save the frame
    path = os.path.abspath(gps[consts.algofolder].val + gps[consts.algoversion].val + "/" + str(cycleid) + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def run_algorithm(gps, cycleid, video):
    algoplfpath = create_algorithm_output_path(gps, cycleid, video)
    paramspath = create_params_output_path(gps, cycleid)
    # UniformMattingCA.exe -CA params.xml contour.ctr image-0001.jpg -avic -r25 -mp4 output.avi
    algocommand = gps[consts.algofolder].val + gps[consts.algoversion].val + '/' +  'UniformMattingCA.exe -CA ' \
    + paramspath + '/' + consts.paramsxml + ' ' \
    + video.path + '/' + video.videoname + '.ctr ' \
    + ' ' + video.path + '/' + 'Frames' + '/image-0001.jpg -avic -r25 -mp4 ' \
    + algoplfpath + '/' + 'output.avi'
    os.system(algocommand)



    try:
        result = subprocess.call(algocommand, stderr=subprocess.STDOUT, shell=True)
        log_information(str(result))
        # subprocess.call([algocommand])
        # uploadfiletos3('homage-automation', 'Output/' + algoversion + "/" + str(cycleid)
        # + "/" + video.videoname + '/' + 'output.avi', outputpath)
    except OSError as e:
        log_information(str(e.args).replace("'",""))

    # uploadfiletos3('homage-automation', 'Output/' + algoversion + "/" + str(cycleid)
        # + "/" + video.videoname + '/' + 'output.avi', outputpath)

    outputplf = get_plf_file(algoplfpath)
    if outputplf:
        return algoplfpath + '/' + outputplf
    return None
