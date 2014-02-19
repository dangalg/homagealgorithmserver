import os
from file import fileIO
from logic.logic_services import general_param_logic

__author__ = 'danga_000'


def create_algorithm_output_path(cycleid, video):
    # Create the path to save the frame
    gps = general_param_logic.get_general_params()
    path = os.path.abspath(gps['VideoFolder'] + gps['AlgorithmOutput'] + "/" + gps['AlgorithmVersion'] + "/" + str(cycleid)
        + "/" + video.videoname.split('.')[0] + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def run_algorithm(cycleid, video, frames):
    path = create_algorithm_output_path(cycleid, video)
    # run algorithm on all frames and return them
    algofiles = []
    for i in range(1,len(frames) + 1):
        # Run Algorithm on frames and save to output folder
        algofilepath = path + "\\" + "output_result" + '{0:04}'.format(i) + ".txt"
        # write all result files to output folder
        file = fileIO.get_file_by_name_write(algofilepath)
        file.write("00======>")
        algofiles.append(file)
    return algofiles