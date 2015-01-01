import subprocess
import math
from algorithm.algorithm import run_algorithm
from compare.compare import run_compare_on_frame
from file.fileIO import get_plf_file
from logic.logic_services.auto_run_video_frame_logic import insert_autorunvideoframe
from logic.logic_services.auto_run_video_logic import insert_autorunvideo
from models.autorunvideo import AutoRunVideo
from models.autorunvideoframe import AutoRunVideoFrame
from utils import log
from utils import consts
__author__ = 'danga_000'

import os

def run_algorithm_then_compare(gps, cycleid, video):
    # create auto video for insert in database
    autovideo = AutoRunVideo(cycleid,video.videoid, 0, "Not Initialized", 0, 0)
    try:
        # create algorithm files
        algoplf = run_algorithm(gps,cycleid,video)
        # get gt file
        saymaplf = get_plf_file(video.path)
        if saymaplf:
            saymaplf = video.path + '/' + saymaplf

        if algoplf is not None and saymaplf is not None:
            # run compare on video and frame
            score, avgscore, finalvariancescore = run_compare_algorithem_to_gt(gps, cycleid, video, algoplf, saymaplf)
            # save average in auto_run_video
            if finalvariancescore == 0:
                autovideo.avexception = "compare error"
                log.log_information(autovideo.avexception)
                print("*********** compare error ********")
            else:
                autovideo.averagescore = avgscore
                autovideo.variancescore = finalvariancescore
                autovideo.finalscore = score
                autovideo.avexception = "good"
                log.log_information(autovideo.avexception)
        elif algoplf is None:
            # If not same frame count return exception
            autovideo.avexception = "No algorithm file"
            log.log_information(autovideo.avexception)
            print("********** No algorithm file ***********")
        elif saymaplf is None:
            autovideo.avexception = "No .plf file"
            log.log_information(autovideo.avexception)
            print("************* No .plf file ************")
    except IOError as e:
        autovideo.averagescore = 0
        videoerror = str(e.args).replace("'", "")
        shortenederror = (videoerror[:600] + '..') if len(videoerror) > 600 else videoerror
        autovideo.avexception = shortenederror
        log.log_information(videoerror)
    # return auto_run
    insert_autorunvideo(autovideo)
    return autovideo


def run_compare_algorithem_to_gt(gps, cycleid, video, algoplf, saymaplf):

    comparefile = gps[consts.outputfolder].val + gps[consts.algoversion].val + '/' + str(cycleid) + '/' \
                  + video.videoname + '/' + 'compare.txt'
    #Algo_Path Countour_Path First_Frame_Path -bmp Output_Path
    comparecommand = gps[consts.algofolder].val + 'PlfComapreCA.exe ' \
    + algoplf + ' ' \
    + saymaplf + ' ' \
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
            except (IndexError, IOError) as e:
                frameerror = "Failed to test frame: " + str(linecounter) + " For Video: " + str(video.videoname) + \
                             " from cycle: " + str(cycleid) + " Error: " + str(e.args).replace("'", "")
                shortenederror = (frameerror[:600] + '..') if len(frameerror) > 600 else frameerror
                autoframe = AutoRunVideoFrame(cycleid, video.videoid, linecounter, 0, shortenederror)
                insert_autorunvideoframe(autoframe)
                log.log_information(frameerror)

    # TODO save to database
    if linecounter != 0:
        avgscore = avgscore/linecounter
        variantavgscore = variance / linecounter
        # TODO save to database
        finalvariancescore = math.sqrt(variantavgscore - avgscore * avgscore)

        return (avgscore - finalvariancescore), avgscore, finalvariancescore
    else:
        return 0,0,0

