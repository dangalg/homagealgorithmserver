import os
from file import fileIO
from file.fileIO import list_frames_by_path, list_gt_frames_by_path
from logic.logic_services import general_param_logic

__author__ = 'danga_000'


def create_algorithm_output_path(cycleid, video, algoversion):
    # Create the path to save the frame
    # path = os.path.abspath(algooutput + algoversion + "/" + str(cycleid)
    #     + "/" + video.videoname + "/")
    path = os.path.abspath(video.path + "/" + algoversion + "/"  + str(cycleid) + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def create_params_output_path(algofolder, cycleid, algoversion):
    # Create the path to save the frame
    path = os.path.abspath(algofolder + "/" + algoversion + "/" + str(cycleid) + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def run_algorithm(cycleid, video, algofolder, algoversion):
    path = create_algorithm_output_path(cycleid, video, algoversion)
    paramspath = create_params_output_path(algofolder, cycleid, algoversion)
    # UniformMattingCA.exe -CA params.xml contour.ctr image-0001.jpg -avic -r25 -mp4 output.avi
    algocommand = algofolder + algoversion + '/' +  'UniformMattingCA.exe -CA ' \
    + paramspath + '/' + 'params.xml ' \
    + video.path + '/' + video.videoname + '.ctr ' \
    + ' ' + video.path + '/' + 'Frames' + '/image-0001.jpg -avic -r25 -mp4 ' \
    + path + '/' + 'output.avi'
    os.system(algocommand)


    outputplf = list_gt_frames_by_path(path)
    return outputplf