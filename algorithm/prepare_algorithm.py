import subprocess
import math
from algorithm.algorithm import run_algorithm
from compare.compare import run_compare_on_frame
from file.fileIO import get_plf_file
from logic.logic_services.auto_run_video_frame_logic import insert_autorunvideoframe, \
    delete_autorunvideoframes_by_cycleidvideoid
from logic.logic_services.auto_run_video_logic import insert_autorunvideo, get_autorunvideo_by_cycleidvideoid, \
    update_autorunvideo
from logic.logic_services.crash_run_video_logic import insert_crashrunvideo, update_crashrunvideo, \
    get_crashrunvideo_by_cycleidvideoid
from models.autorunvideo import AutoRunVideo
from models.autorunvideoframe import AutoRunVideoFrame
from models.crash_run_video import CrashRunVideo
from utils import log
from utils import consts
__author__ = 'danga_000'

import os
from subprocess import Popen, PIPE

def run_algorithm_then_compare(run, gps, cycleid, video):
    crashcount = 0
    if not gps[consts.crashrunname].val:
        foundautovideo = False
        autovideo = get_autorunvideo_by_cycleidvideoid(cycleid,video.videoid)
        if autovideo:
            foundautovideo = True
            if autovideo.avexception != "good" and not gps[consts.updatedbname].val:
                crashcount += 1
        if gps[consts.updatedbname].val or not autovideo:
            # create auto video for insert in database
            autovideo = AutoRunVideo(cycleid,video.videoid, 0, "Not Initialized", 0, 0, 'None')
            try:
                # create algorithm files
                algoplf, awsplf, result= run_algorithm(gps,cycleid,video)
                # get gt file
                saymaplf = get_plf_file(video.path)
                if saymaplf:
                    saymaplf = video.path + '/' + saymaplf

                if algoplf and saymaplf and result == "good":
                    # run compare on video and frame
                    score, avgscore, finalvariancescore, result = run_compare_algorithem_to_gt(gps, cycleid, video, algoplf, saymaplf)
                    # save average in auto_run_video
                    if finalvariancescore == 0 or result != "good":
                        autovideo.avexception = "compare error: " + str(result).replace("'","")
                        log.log_information(gps, autovideo.avexception)
                        print("*********** compare error ********\n" + str(result).replace("'",""))
                        crashcount += 1
                    else: # Success
                        autovideo.averagescore = avgscore
                        autovideo.variancescore = finalvariancescore
                        autovideo.finalscore = score
                        autovideo.avexception = "good"
                        log.log_information(gps, autovideo.avexception)
                        autovideo.awsoutput = awsplf
                elif algoplf is None:
                    # If not same frame count return exception
                    autovideo.avexception = "No algorithm file"
                    log.log_information(gps, autovideo.avexception)
                    print("********** No algorithm file ***********")
                    crashcount += 1
                elif saymaplf is None:
                    autovideo.avexception = "No .plf file"
                    log.log_information(gps, autovideo.avexception)
                    print("************* No .plf file ************")
                    crashcount += 1
                elif result != "good":
                    autovideo.avexception = result.replace("'","")
                    log.log_information(gps, autovideo.avexception)
                    print(result.replace("'",""))
                    crashcount += 1
            except IOError as e:
                videoerror = str(e.args).replace("'", "")
                shortenederror = (videoerror[:600] + '..') if len(videoerror) > 600 else videoerror
                autovideo.avexception = shortenederror
                log.log_information(gps, videoerror)
            # return auto_run
            if foundautovideo:
                update_autorunvideo(autovideo)
            else:
                insert_autorunvideo(autovideo)
        return autovideo, crashcount
    else:
        foundcrashvideo = False
        crashrunvideo = get_crashrunvideo_by_cycleidvideoid(cycleid,video.videoid)
        if crashrunvideo:
            foundcrashvideo = True
        crashrunvideo = CrashRunVideo(cycleid, video.videoid, "Not Initialized")
        algoplf, awsplf, result = run_algorithm(gps,cycleid,video)
        if algoplf and result == "good":
            crashrunvideo.crvexception = 'good'
        else:
            crashrunvideo.crvexception = 'Algorithem malfunctioned: ' + str(result).replace("'","")
            crashcount += 1
        if foundcrashvideo:
            update_crashrunvideo(crashrunvideo)
        else:
            insert_crashrunvideo(crashrunvideo)
        return crashrunvideo, crashcount


def run_compare_algorithem_to_gt(gps, cycleid, video, algoplf, saymaplf):
    delete_autorunvideoframes_by_cycleidvideoid(cycleid, video.videoid)
    comparefile = gps[consts.outputfoldername].val + gps[consts.algoversionname].val + '/' + str(cycleid) + '/' \
                  + video.videoname + '/' + 'compare.txt'
    #Algo_Path Countour_Path First_Frame_Path -bmp Output_Path
    comparecommand = gps[consts.algofoldername].val + 'PlfComapreCA.exe ' \
    + algoplf + ' ' \
    + saymaplf + ' ' \
    + comparefile
    os.system(comparecommand)

    cmd = comparecommand
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    print("message: " + str(stdout))
    print("error: " + str(stderr))
    result = "good"
    if "failed" in str(stderr):
        result = str(stderr)

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
                frameerror = str(e.args).replace("'", "")
                shortenederror = (frameerror[:600] + '..') if len(frameerror) > 600 else frameerror
                autoframe = AutoRunVideoFrame(cycleid, video.videoid, linecounter, 0, shortenederror)
                insert_autorunvideoframe(autoframe)
                log.log_information(gps, frameerror)

    if linecounter != 0:
        avgscore = avgscore/linecounter
        variantavgscore = variance / linecounter
        finalvariancescore = math.sqrt(variantavgscore - avgscore * avgscore)

        return (avgscore - finalvariancescore), avgscore, finalvariancescore, result
    else:
        return 0,0,0, result

