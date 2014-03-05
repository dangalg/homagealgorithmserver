import os
from file import fileIO
from file.fileIO import list_frames_by_path
from logic.logic_services import general_param_logic

__author__ = 'danga_000'


def create_algorithm_output_path(cycleid, video, algooutput, algoversion):
    # Create the path to save the frame
    path = os.path.abspath(algooutput + algoversion + "/" + str(cycleid)
        + "/" + video.videoname + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def run_algorithm(cycleid, video, frames, algooutput, algofolder, algoversion):
    path = create_algorithm_output_path(cycleid, video, algooutput,algoversion)
    # run algorithm on all frames and return them
    algocommand = algofolder + algoversion + '/' + 'UniformMattingCA.exe ' \
    + video.path + '/' + video.videoname + '.ctr ' \
    + 'C:/Dummy.ebox ' + video.path + '/' + 'Frames' + '/image-0001.jpg -bmp ' \
    + path + '\\' + 'image-0001.bmp'
    os.system(algocommand)


    algofiles = list_frames_by_path(path)
    return algofiles