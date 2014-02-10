__author__ = 'danga_000'

from logic.logic_services import video
from file import fileIO
import os
from logic.logic_services import general_param
import algorithm


def run_compare(video):
    # get video frames
    frames , framenum = video.get_all_frames_from_video(video)
    # get test frames
    testframes = video.get_all_test_frames_from_video(video,framenum)
    run_test_on_frames(video,frames,testframes,framenum)
    # run test on every frame and save in auto_run_video_frame
    # save average in auto_run_video
    # return auto_run
    pass

def run_test_on_frames(video, frames,testframes,framenum):
    for i in range(1,framenum):
        compare_frame_to_testframe(video,frames(i),testframes(i),i)


def compare_frame_to_testframe(video, frame, testframe, i):
    gps = general_param.get_general_params()
    path = gps['AlgorithmOutput'] + "\\" + gps['AlgorithmVersion']
    os.mkdir(path)
    file = fileIO.get_file_by_name_write(path + video.videoname + "output_result" + '{0:03}'.format(i))
    algorithm.run_algorith_on_frame(file,frame,testframe)

