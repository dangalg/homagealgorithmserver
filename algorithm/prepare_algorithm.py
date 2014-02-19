from algorithm.algorithm import run_algorithm
from compare.compare import run_compare_on_frame
from file import fileIO
from logic.logic_services.auto_run_video_frame_logic import insert_update_autorunvideoframe
from logic.logic_services.auto_run_video_logic import insert_update_autorunvideo
from logic.logic_services.video_logic import get_all_gt_files_from_video, get_all_frames_from_video
from models.autorunvideo import AutoRunVideo
from models.autorunvideoframe import AutoRunVideoFrame
from utils import log

__author__ = 'danga_000'

import os
from logic.logic_services import general_param_logic


def run_algorithm_then_compare(cycleid, video, params):
    # create auto video for insert in database
    autovideo = AutoRunVideo(cycleid,video.videoid, 0, "Not Initialized")
    try:
        # get video frames
        frames = get_all_frames_from_video(video)
        # create algorithm files
        algofiles = run_algorithm(cycleid,video,frames)
        # get gt frames
        gtfiles = get_all_gt_files_from_video(video)
        # run compare on every frame and save in auto_run_video_frame
        avgscore = run_compare_on_frames(cycleid, video, algofiles, gtfiles, params)
        # save average in auto_run_video
        autovideo.averagescore = avgscore
        autovideo.avexception = "good"
    except IOError:
        autovideo.averagescore = 0
        autovideo.avexception = "Failed to test Video: " + str(video.videoid) + " from cycle: " + str(cycleid)
        log.log_errors("Failed to test Video: " + str(video.videoid) + " from cycle: " + str(cycleid))
    # return auto_run
    if autovideo.avexception == "good":
        insert_update_autorunvideo(autovideo)
        return autovideo


def run_compare_on_frames(cycleid, video, algofiles, gtfiles, params):
    score = 0
    for i in range(0,video.numofframes - 1):
        try:
            score = score + run_compare_frame_to_testframe(cycleid,video,algofiles[i],gtfiles[i],i,params)
        except IOError:
            log.log_errors("Failed to test frame: " + str(i) +" For Video: " + str(video.videoname) + " from cycle: " + str(cycleid))
    if video.numofframes != 0:
        avgscore = score / video.numofframes
        return avgscore


def run_compare_frame_to_testframe(cycleid, video, algofile, gtfile, i, params):
    score = run_compare_on_frame(algofile, gtfile, params)
    # create and save frame to database
    autoframe = AutoRunVideoFrame(cycleid, video.videoid, i, score)
    insert_update_autorunvideoframe(autoframe)
    return score

