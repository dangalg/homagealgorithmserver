import subprocess
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


def run_algorithm_then_compare(cycleid, video, algooutput, algofolder, algoversion, params):
    # create auto video for insert in database
    autovideo = AutoRunVideo(cycleid,video.videoid, 0, "Not Initialized")
    try:
        # get video frames
        frames = get_all_frames_from_video(video)
        # create algorithm files
        algofiles = run_algorithm(cycleid,video,frames,algooutput, algofolder, algoversion, params)
        # get gt frames
        gtfiles = get_all_gt_files_from_video(video)

        if len(algofiles) == len(gtfiles):
            # run compare on every frame and save in auto_run_video_frame
            avgscore = run_compare_on_frames(cycleid, video, algooutput, algofolder, algoversion, algofiles, gtfiles, params)
            # save average in auto_run_video
            autovideo.averagescore = avgscore
            autovideo.avexception = "good"
        else:
            # If not same frame count return exception
            autovideo.averagescore = 0
            autovideo.avexception = "Not same number of algorithm files and GT files"
    except IOError:
        autovideo.averagescore = 0
        autovideo.avexception = "Failed to test Video: " + str(video.videoid) + " from cycle: " + str(cycleid)
        log.log_errors("Failed to test Video: " + str(video.videoid) + " from cycle: " + str(cycleid))
    # return auto_run
    insert_update_autorunvideo(autovideo)
    return autovideo


def run_compare_on_frames(cycleid, video, algooutput, algofolder, algoversion, algofiles, gtfiles, params):
    score = 0
    framecount = video.numofframes
    # for i in range(0,algofiles.count()):
    try:
        framescore = run_compare_frame_to_testframe(cycleid,video, algooutput, algofolder, algoversion, algofiles[0],gtfiles[0],0,params)
        if framescore != 0:
            score = score + framescore
        else:
            framecount -= 1
    except IOError:
        log.log_errors("Failed to test frame: " + str(0) +" For Video: " + str(video.videoname) + " from cycle: " + str(cycleid))
        framecount -= 1
    if video.numofframes != 0:
        if framecount != 0:
            avgscore = score #/ framecount
        else:
            avgscore = 0
        return avgscore


def run_compare_frame_to_testframe(cycleid, video, algooutput, algofolder, algoversion, plffile, gtfile, i, params):

    comparefile = algooutput + algoversion + '/' + str(cycleid) + '/' + video.videoname + '/' + 'compare.txt'
    #Algo_Path Countour_Path First_Frame_Path -bmp Output_Path
    comparecommand = algofolder + '/' +  'PlfComapreCA.exe ' \
    + algooutput + algoversion + '/' + str(cycleid) + '/' + video.videoname + '/'  + plffile + ' ' \
    + video.path + '/' + gtfile + ' ' \
    + comparefile
    os.system(comparecommand)

    framecount = 0
    avgscore = 0
    linecounter = 0
    with open(comparefile,'r') as f:
        for x in f:
            linecounter = linecounter+1
            x = x.replace('     ', ' ')
            x = x.replace('    ', ' ')
            x = x.replace('   ', ' ')
            x = x.replace('  ', ' ')
            values = x.split(' ')
            framenum = values[0]
            avgdistX =values[1]
            avgdistY = values[2]
            varX  = values[3]
            varY  = values[4]
            pctX  = values[5]
            pctY = values[6]
            pctY = pctY.replace('\n', '')
            score = run_compare_on_frame(framenum, avgdistX, avgdistY, varX, varY, pctX, pctY)
            # create and save frame to database
            autoframe = AutoRunVideoFrame(cycleid, video.videoid, i, score)
            insert_update_autorunvideoframe(autoframe)
            framecount = framecount+1
            avgscore = avgscore + score

    return (avgscore/linecounter)

