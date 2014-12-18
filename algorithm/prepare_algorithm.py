import subprocess
import math
from algorithm.algorithm import run_algorithm
from compare.compare import run_compare_on_frame
from logic.logic_services.auto_run_video_frame_logic import insert_autorunvideoframe
from logic.logic_services.auto_run_video_logic import insert_autorunvideo
from logic.logic_services.video_logic import get_all_gt_files_from_video
from models.autorunvideo import AutoRunVideo
from models.autorunvideoframe import AutoRunVideoFrame
from utils import log

__author__ = 'danga_000'

import os

def run_algorithm_then_compare(cycleid, video, algofolder, algoversion, params):
    # create auto video for insert in database
    autovideo = AutoRunVideo(cycleid,video.videoid, 0, "Not Initialized", 0, 0)
    try:
        # create algorithm files
        algofile = run_algorithm(cycleid,video,algofolder, algoversion)
        # get gt file
        gtfile = get_all_gt_files_from_video(video)

        if len(algofile) != 0 and len(gtfile) != 0:
            # run compare on video and frame
            score, avgscore, finalvariancescore = run_compare_algorithem_to_gt(cycleid, video, algofolder, algoversion, algofile, gtfile)
            # save average in auto_run_video
            autovideo.averagescore = avgscore
            autovideo.variancescore = finalvariancescore
            autovideo.finalscore = score
            autovideo.avexception = "good"
        elif len(algofile) == 0:
            # If not same frame count return exception
            autovideo.averagescore = 0
            autovideo.avexception = "No algorithm file"
        elif len(gtfile) == 0:
            autovideo.averagescore = 0
            autovideo.avexception = "No .plf file"
    except IOError as e:
        autovideo.averagescore = 0
        videoerror = "Failed to test Video: " + str(video.videoid) + " from cycle: " + str(cycleid) + " Error: " \
                     + e.args
        shortenederror = (videoerror[:600] + '..') if len(videoerror) > 600 else videoerror
        autovideo.avexception = shortenederror
        log.log_errors(videoerror)
    # return auto_run
    insert_autorunvideo(autovideo)
    return autovideo


def run_compare_algorithem_to_gt(cycleid, video, algofolder, algoversion, plffile, gtfile):

    comparefile = video.path + '/' + algoversion + '/' + str(cycleid) + '/' + 'compare.txt'
    #Algo_Path Countour_Path First_Frame_Path -bmp Output_Path
    comparecommand = algofolder + 'PlfComapreCA.exe ' \
    + video.path + '/' + algoversion + '/'  + str(cycleid) + '/'  + plffile + ' ' \
    + video.path + '/' + gtfile + ' ' \
    + comparefile
    os.system(comparecommand)

    avgscore = 0
    linecounter = 0
    variance = 0
    i = 0
    with open(comparefile,'r') as f:
        for x in f:
            try:
                linecounter += 1
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
                autoframe = AutoRunVideoFrame(cycleid, video.videoid, linecounter, score, "good")
                insert_autorunvideoframe(autoframe)
                avgscore = avgscore + score
                variance += score * score
                i += 1
            except IOError as e:
                frameerror = "Failed to test frame: " + str(linecounter) + " For Video: " + str(video.videoname) + \
                             " from cycle: " + str(cycleid) + " Error: " + e.args
                shortenederror = (frameerror[:600] + '..') if len(frameerror) > 600 else frameerror
                autoframe = AutoRunVideoFrame(cycleid, video.videoid, linecounter, 0, shortenederror)
                insert_autorunvideoframe(autoframe)
                log.log_errors(frameerror)

    # TODO save to database
    avgscore = avgscore/linecounter
    variantavgscore = variance / linecounter
    # TODO save to database
    finalvariancescore = math.sqrt(variantavgscore - avgscore * avgscore)

    return (avgscore - finalvariancescore), avgscore, finalvariancescore

