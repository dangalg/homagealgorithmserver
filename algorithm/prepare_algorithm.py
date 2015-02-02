import subprocess
import math
from algorithm.algorithm import run_algorithm, create_algorithm_output_path
from compare.compare import run_compare_on_frame
from data.aws_helper import uploadfiletos3
from file import zippy
from file.fileIO import get_plf_file
from logic.logic_services import auto_run_video_logic
from logic.logic_services.auto_run_video_frame_logic import insert_autorunvideoframe, \
    delete_autorunvideoframes_by_cycleidvideoid
from logic.logic_services.auto_run_video_logic import insert_autorunvideo, get_autorunvideo_by_cycleidvideoid, \
    update_autorunvideo
from logic.logic_services.auto_run_video_frame_logic import get_new_autorunvideoframe_id
from logic.logic_services.crash_run_video_logic import insert_crashrunvideo, update_crashrunvideo, \
    get_crashrunvideo_by_cycleidvideoid, get_new_crashrunvideo_id
from models.autorunvideo import AutoRunVideo
from models.autorunvideoframe import AutoRunVideoFrame
from models.crash_run_video import CrashRunVideo
from utils import log
from utils import consts
__author__ = 'danga_000'

import os
from subprocess import Popen, PIPE


def create_auto_run_video(autovideo, crashcount, cycleid, foundautovideo, gps, video):
    autovideo = AutoRunVideo(auto_run_video_logic.get_new_autorunvideo_id(), cycleid, video.videoid, -1, "Not Initialized", -1, -1, 'None')
    try:
        # create algorithm files
        algoplf, result, s3_url = run_algorithm(gps, cycleid, video)
        # get gt file
        saymaplf = get_plf_file(video.path)
        if saymaplf:
            saymaplf = video.path + '/' + saymaplf

        if algoplf and saymaplf and result == "good":
            # run compare on video and frame
            score, avgscore, finalvariancescore, result = run_compare_algorithem_to_gt(gps, cycleid, video, algoplf,
                                                                                       saymaplf)
            # save average in auto_run_video
            if finalvariancescore == 0 or result != "good":
                autovideo.avexception = "compare error: " + str(result).replace("'", "")
                log.log_information(gps, autovideo.avexception)
                print("*********** compare error ********\n" + str(result).replace("'", ""))
                crashcount += 1
            else:  # Success
                autovideo.averagescore = avgscore
                autovideo.variancescore = finalvariancescore
                autovideo.finalscore = score
                autovideo.avexception = "good"
                log.log_information(gps, autovideo.avexception)
                if s3_url:
                    autovideo.awsoutput = s3_url
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
            autovideo.avexception = result.replace("'", "")
            log.log_information(gps, autovideo.avexception)
            print(result.replace("'", ""))
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


def create_crash_run_video(crashcount, cycleid, gps, video):
    foundcrashvideo = False
    crashrunvideo = get_crashrunvideo_by_cycleidvideoid(cycleid, video.videoid)
    if crashrunvideo:
        foundcrashvideo = True
    crashrunvideo = CrashRunVideo(get_new_crashrunvideo_id(), cycleid, video.videoid, "Not Initialized")
    algoplf, result, s3_url = run_algorithm(gps, cycleid, video)
    if algoplf and result == "good":
        crashrunvideo.crvexception = 'good'
    else:
        crashrunvideo.crvexception = 'Algorithem malfunctioned: ' + str(result).replace("'", "")
        crashcount += 1
    if foundcrashvideo:
        update_crashrunvideo(crashrunvideo)
    else:
        insert_crashrunvideo(crashrunvideo)
    return crashcount, crashrunvideo


def run_algorithm_then_compare(run, gps, cycleid, video):
    crashcount = 0
    if not gps[consts.crashrunname].val:
        foundautovideo = False
        autovideo = get_autorunvideo_by_cycleidvideoid(cycleid,video.videoid)
        if autovideo:
            foundautovideo = True
        if gps[consts.updatedbname].val or not autovideo or autovideo.avexception != "good" \
                or any(video.videoname in s for s in gps[consts.remakelistname].val):
            # create auto video for insert in database
            autovideo, crashcount = create_auto_run_video(autovideo, crashcount, cycleid, foundautovideo, gps, video)
        return autovideo, crashcount
    else:
        crashcount, crashrunvideo = create_crash_run_video(crashcount, cycleid, gps, video)
        return crashrunvideo, crashcount


def run_auto_video_frames(avgscore, comparefile, cycleid, gps, i, linecounter, variance, video):

    algoplfpath = create_algorithm_output_path(gps, cycleid, video)

    awsoutputpath = 'Output/' + gps[consts.algoversionname].val + "/" + str(cycleid) + "/" + video.videoname


    # zip output folder and Upload to s3
    print("Zipping: " + str(algoplfpath))
    zippy.zip_video_folder(algoplfpath, algoplfpath)
    print("Uploading: " + str(algoplfpath))
    uploadfiletos3(consts.awsautomationbucket,
                              awsoutputpath + '.zip',
                              algoplfpath + '.zip')


    # Calculate Score
    with open(comparefile, 'r') as f:
        for x in f:
            try:
                linecounter += 1
                x = x.replace('     ', ' ')
                x = x.replace('    ', ' ')
                x = x.replace('   ', ' ')
                x = x.replace('  ', ' ')
                values = x.split(' ')
                framenum = values[0]
                avgdistX = values[1]
                avgdistY = values[2]
                varX = values[3]
                varY = values[4]
                pctX = values[5]
                pctY = values[6]
                pctY = pctY.replace('\n', '')
                score = run_compare_on_frame(framenum, float(avgdistX), float(avgdistY), float(varX), float(varY), float(pctX), float(pctY))
                # create and save frame to database
                autoframe = AutoRunVideoFrame(get_new_autorunvideoframe_id(), cycleid, video.videoid, linecounter, score, "good")
                insert_autorunvideoframe(autoframe)
                avgscore = avgscore + score
                variance += score * score
                i += 1
            except (IndexError, IOError) as e:
                frameerror = str(e.args).replace("'", "")
                shortenederror = (frameerror[:600] + '..') if len(frameerror) > 600 else frameerror
                autoframe = AutoRunVideoFrame(get_new_autorunvideoframe_id(), cycleid, video.videoid, linecounter, 0, shortenederror)
                insert_autorunvideoframe(autoframe)
                log.log_information(gps, frameerror)
    return avgscore, linecounter, variance


def run_compare_algorithem_to_gt(gps, cycleid, video, algoplf, saymaplf):
    delete_autorunvideoframes_by_cycleidvideoid(cycleid, video.videoid)
    comparefile = gps[consts.outputfoldername].val + gps[consts.algoversionname].val + '/' + str(cycleid) + '/' \
                  + video.videoname + '/' + 'compare.txt'
    #Algo_Path Countour_Path First_Frame_Path -bmp Output_Path
    comparecommand = gps[consts.comparefilepathname].val + ' ' \
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
    avgscore, linecounter, variance = run_auto_video_frames(avgscore, comparefile, cycleid, gps, i, linecounter,
                                                            variance, video)

    if linecounter != 0:
        avgscore = avgscore/linecounter
        variantavgscore = variance / linecounter
        finalvariancescore = math.sqrt(variantavgscore - avgscore * avgscore)

        finalscore = (avgscore - finalvariancescore)
        if finalscore < 0:
            finalscore = 0
        return finalscore, avgscore, finalvariancescore, result
    else:
        return 0,0,0, result

