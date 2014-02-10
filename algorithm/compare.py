from logic.logic_services.auto_run import get_top_cycle_id
from logic.logic_services.auto_run_video import insert_autorunvideo
from logic.logic_services.auto_run_video_frame import insert_autorunvideoframe
from models.autorunvideo_model import AutoRunVideo
from models.autorunvideoframe_model import AutoRunVideoFrame
from utils import log

__author__ = 'danga_000'

from file import fileIO
import os
from logic.logic_services import general_param
import algorithm


def run_compare(video):
    cycleid = get_top_cycle_id() + 1
    # create auto video for insert in database
    autovideo = AutoRunVideo()
    autovideo.cycleid = cycleid
    autovideo.videoid = video.videoid
    try:
        # get video frames
        frames , framenum = video.get_all_frames_from_video(video)
        # get test frames
        testframes = video.get_all_test_frames_from_video(video,framenum)
        # run test on every frame and save in auto_run_video_frame
        avgscore = run_test_on_frames(cycleid, video,frames,testframes,framenum)
        # save average in auto_run_video
        autovideo.averagescore = avgscore
        autovideo.exception = None
    except IOError:
        autovideo.averagescore = 0
        autovideo.exception = "Failed to test Video: " + str(video.videoid) + " from cycle: " + str(cycleid)
        log.log_errors("Failed to test Video: " + str(video.videoid) + " from cycle: " + str(cycleid))
    # return auto_run
    insert_autorunvideo(autovideo)
    return autovideo


def run_test_on_frames(cycleid, video, frames,testframes,framenum):
    score = 0
    for i in range(1,framenum):
        score = score + compare_frame_to_testframe(cycleid,video,frames(i),testframes(i),i)
    avgscore = score / framenum
    return avgscore


def compare_frame_to_testframe(cycleid, video, frame, testframe, i):
    gps = general_param.get_general_params()
    path = gps['AlgorithmOutput'] + "\\" + gps['AlgorithmVersion']
    os.mkdir(path)
    file = fileIO.get_file_by_name_write(path + video.videoname + "output_result" + '{0:03}'.format(i))
    score = algorithm.run_algorithem_on_frame(file,frame,testframe)
    # create and save frame to database
    autoframe = AutoRunVideoFrame()
    autoframe.cycleid = cycleid
    autoframe.videoid = video.videoid
    autoframe.frameid = i
    autoframe.score = score
    insert_autorunvideoframe(autoframe)
    return score

