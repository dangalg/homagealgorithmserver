import datetime
import itertools
import os
from tkinter import END
from algorithm.algorithm import create_params_output_path

from algorithm.prepare_algorithm import run_algorithm_then_compare
from data.aws_helper import downloadfilefroms3, downloadfolderfroms3
from file import fileIO
from logic.logic_services import crash_run_logic
from logic.logic_services import auto_run_logic
from logic.logic_services.auto_run_logic import get_autorun_by_algorithem_params
from logic.logic_services.crash_run_logic import get_crashrun_by_algorithem_params
from logic.logic_services.general_param_logic import insert_update_general_param
from logic.logic_services.parameter_logic import insert_param
from logic.logic_services.video_logic import insert_update_videos_from_path
from models.autorun import AutoRun
from models.crash_run import CrashRun
from models.generalparam import GeneralParam
from models.parameter import Parameter
from utils import log
from utils import consts
from logic.logic_services.parameter_logic import get_new_param_id


__author__ = 'danga_000'


def run_cycle(crashrun, optimize, updatedb, algoversion, mainfolder, remakelist):

    print("Setting params...")
    gps = set_user_info(crashrun, optimize, updatedb, algoversion,mainfolder,remakelist)

    # Download Algorithem from S3
    downloadfolderfroms3(consts.awsautomationbucket, consts.awsalgorithem + gps[consts.algoversionname].val, gps[consts.mainfoldername].val)
    # Download Compare File
    downloadfilefroms3(consts.awsautomationbucket ,consts.awsalgorithem + consts.comparefile, gps[consts.comparefilepathname].val)

     # get existing videos automatically from their folder and aws and insert to database if needed
    videos = insert_update_videos_from_path(gps)
    numofvideos = len(videos)
    permutationparams = getParamsFromFile(gps)
    paramlists = get_params_list(gps[consts.optimizationname].val,permutationparams)
    if gps[consts.optimizationname].val:
        permutationlist = list(itertools.product(*paramlists))
    else:
        permutationlist = paramlists
    # ----cycle through params------
    for i in range(0, len(permutationlist)):
        params = create_params(i, permutationlist, permutationparams)
        cycleid, run = get_cycle_id(crashrun, gps, params)
        print("Starting Run Cycle " + str(cycleid))
        write_params_to_file(cycleid, gps, params) # run cycle on all videos:
        print("running " + str(i) + " permutation: " + str(permutationlist[i]))
        startdate= datetime.datetime.now()
        run_video_cycle(gps, cycleid, numofvideos, startdate, videos, run, params)

    print("*********** FINISHED **************")


def run_video_cycle(gps, cycleid, numofvideos, startdate, videos, run, params):
    crashcount = 0
    if not gps[consts.crashrunname].val:
        videocount = numofvideos
        i=2
        avgscore = 0
        for video in videos:
            i = i+1
            print("Testing " + video.videoname)
            try:
                autovideo, crashnum = run_algorithm_then_compare(run, gps, cycleid, video)
                crashcount += crashnum
                if autovideo.avexception == 'good':
                    avgscore = avgscore + autovideo.finalscore
                    print("Score: " + str(autovideo.finalscore))
                else:
                    videocount -= 1
            except IOError as e:
                log.log_information(gps, str(e.args).replace("'",""))
                videocount -= 1
                print(str(e.args).replace("'",""))
        # Save average score
        if videocount != 0:
            avgscore = avgscore / videocount
        else:
            avgscore = 0
        # create auto_run with params
        ar = AutoRun(run.cycleid, run.algoversion, run.params, run.startdate, datetime.datetime.now(), avgscore, crashcount)
        # Save autorun info
        auto_run_logic.update_autorun(ar)
        save_avgscore_to_report(gps, avgscore, cycleid)
        print("**** Finished Cycle " + str(cycleid) + " Score: " + str(avgscore) + " ****")
    else:
        for video in videos:
            print("Crash Testing " + video.videoname)
            crashrunvideo, crashnum = run_algorithm_then_compare(run, gps, cycleid, video)
            crashcount += crashnum
        cr = CrashRun(run.cycleid, run.algoversion, run.params, run.startdate, datetime.datetime.now(), crashcount)
        crash_run_logic.update_crashrun(cr)


# range of floats
def frange(min, max, jump, default):
    paramlist = []
    if jump == 0:
        paramlist.append(str(default))
    else:
        while min < max:
            paramlist.append(str(min))
            min += jump
    return paramlist


def get_params_list(optimize,paramsdb):
    paramlists = []
    paramtuple = ()
    # Get params from database to list
    #paramsdb = get_params_by_algo_version(algoversion)
    # create a list of all parameter values to iterate over for each parameter
    for param in paramsdb:
        if optimize:
            paramlist = frange(int(param.min), int(param.max)+1, int(param.change), int(param.default))
            paramlists.append(paramlist)
        else:
            paramtuple = paramtuple + (param.default,)
    if optimize:
        return paramlists
    else:
        return [paramtuple]


def set_user_info(crashrun, optimize, updatedb, algoversion,mainfolder, remakelist):
    #set Algorithm output and version
    print("Saving folders to database...")
    gps = {}
    gpalgoversion = GeneralParam(consts.algofoldername, str(algoversion))
    gpalgofolder = GeneralParam(consts.algofoldername, str(mainfolder + '/' + consts.algorithem + '/'))
    iscrashrun = False
    if crashrun == '1':
        iscrashrun = True
    crashrunparam = GeneralParam(consts.crashrunname, iscrashrun)
    optimization = False
    if optimize == '1':
        optimization = True
    algorunoptimization = GeneralParam(consts.optimizationname, optimization)
    shouldupdatedb = False
    if updatedb == '1':
        shouldupdatedb = True
    updatedbparam = GeneralParam(consts.crashrunname, shouldupdatedb)
    # if iscrashrun:
    #     videofolder = GeneralParam(consts.crashrunvideofoldername, str(mainfolder + '/' + consts.crashrunvideos + '/'))
    # else:
    videofolder = GeneralParam(consts.videofoldername, str(mainfolder + '/' + consts.videos + '/'))
    crashfolderparam = GeneralParam(consts.crashrunvideofoldername, str(mainfolder + '/' + consts.crashrunvideos + '/'))
    outputfolder = GeneralParam(consts.outputfoldername, str(mainfolder + '/' + consts.output + '/'))
    crashoutputfolder = GeneralParam(consts.crashoutputfoldername, str(mainfolder + '/' + consts.crashoutput + '/'))
    mainfolderparam = GeneralParam(consts.mainfoldername, str(mainfolder + '/'))
    paramsfilename = GeneralParam(consts.paramsfilepathname, gpalgofolder.val + consts.paramsxml)
    comparefilename = GeneralParam(consts.paramsfilepathname, gpalgofolder.val + consts.comparefile)
    remakelistparam = GeneralParam(consts.remakelistname, remakelist)
    insert_update_general_param(gpalgofolder)
    insert_update_general_param(gpalgoversion)
    insert_update_general_param(algorunoptimization)
    insert_update_general_param(videofolder)
    insert_update_general_param(outputfolder)
    insert_update_general_param(crashoutputfolder)
    insert_update_general_param(paramsfilename)
    insert_update_general_param(comparefilename)
    insert_update_general_param(crashrunparam)
    insert_update_general_param(mainfolderparam)
    insert_update_general_param(crashfolderparam)
    insert_update_general_param(updatedbparam)
    insert_update_general_param(remakelistparam)

    gps[consts.mainfoldername] = mainfolderparam
    gps[consts.algoversionname] = gpalgoversion
    gps[consts.algofoldername] = gpalgofolder
    gps[consts.optimizationname] = algorunoptimization
    gps[consts.videofoldername] = videofolder
    gps[consts.outputfoldername] = outputfolder
    gps[consts.crashoutputfoldername] = crashoutputfolder
    gps[consts.paramsfilepathname] = paramsfilename
    gps[consts.comparefilepathname] = comparefilename
    gps[consts.crashrunname] = crashrunparam
    gps[consts.crashrunvideofoldername] = crashfolderparam
    gps[consts.updatedbname] = updatedbparam
    gps[consts.remakelistname] = remakelistparam
    createfolders(gps)
    return gps


def getParamsFromFile(gps):
    # Get params from s3
    downloadfilefroms3(consts.awsautomationbucket ,consts.awsalgorithem + consts.paramsxml, gps[consts.paramsfilepathname].val)

    #  get params from path to params
    parameters = []
    with open(gps[consts.paramsfilepathname].val,'r') as f:
        for x in f:
            row = x.split(',')
            if len(row) == 5:
                param = Parameter(get_new_param_id(), 0, gps[consts.algoversionname].val,row[0],row[1],row[2],row[3],row[4].replace('\n',''))
                parameters.append(param)
                # insert_param(param)
    return parameters


def deleteContent(fName):
    with open(fName, "w"):
        pass


def save_avgscore_to_report(gps, avgscore, cycleid):
    path = os.path.abspath(gps[consts.outputfoldername].val + gps[consts.algoversionname].val + "/" + str(cycleid) + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    file = fileIO.get_file_by_name_write(path + "\\" + "cycle-" + str(cycleid) + "-score.txt")
    file.write(str(avgscore))


def createfolders(gps):
    path = gps[consts.algofoldername].val
    if not os.path.exists(path):
        os.makedirs(path)
    path = gps[consts.videofoldername].val
    if not os.path.exists(path):
        os.makedirs(path)
    path = gps[consts.crashrunvideofoldername].val
    if not os.path.exists(path):
        os.makedirs(path)
    path = gps[consts.outputfoldername].val
    if not os.path.exists(path):
        os.makedirs(path)
    path = gps[consts.crashoutputfoldername].val
    if not os.path.exists(path):
        os.makedirs(path)


def create_params(i, permutationlist, permutationparams):
    params = ''
    params = params + "<UniformBackgroundPrm>"
    for j in range(0, len(permutationparams)):
        params = params + '<' + permutationparams[j].name + '>' + str(permutationlist[i][j]) + '</' + permutationparams[j].name + '>'
    params = params + "</UniformBackgroundPrm>"
    return params


def write_params_to_file(cycleid, gps, params):
    paramsfile = create_params_output_path(gps,cycleid)
    deleteContent(paramsfile)
    with open(paramsfile, "a") as myfile:
        myfile.write(params)


def get_cycle_id(crashrun, gps, params):
    # get new cycle_id
    cycleid = 1
    run = None
    if crashrun == '1':
        cycle_id = crash_run_logic.get_new_cycle_id()
        pcrashrun = CrashRun(cycle_id,gps[consts.algoversionname].val,params,datetime.datetime.now(),datetime.datetime.now(),0)
        crashrun = get_crashrun_by_algorithem_params(pcrashrun)
        if crashrun:
            cycleid = crashrun.cycleid
            run = crashrun
        else:
            cycleid = crash_run_logic.get_new_cycle_id()
            pcrashrun.cycleid = cycleid
            run = pcrashrun
            crash_run_logic.insert_crashrun(run)
    else:
        cycle_id = auto_run_logic.get_new_cycle_id()
        pautorun = AutoRun(cycle_id,gps[consts.algoversionname].val,params,datetime.datetime.now(),datetime.datetime.now(),0,0)
        autorun = get_autorun_by_algorithem_params(pautorun)
        if autorun:
            cycleid = autorun.cycleid
            run = autorun
        else:
            cycleid = auto_run_logic.get_new_cycle_id()
            pautorun.cycleid = cycleid
            run = pautorun
            auto_run_logic.insert_autorun(run)
    return cycleid, run

# def get_starting_general_params():
#     dbgps = general_param_logic.get_general_params()
#     gps = []
#     default = 'Set Folder Please'
#     algoversion = dbgps.get(consts.algoversionname, default)
#     algofolder = dbgps.get(consts.algofoldername, default)
#     crashrun = dbgps.get(consts.crashrunname, '0')
#     if crashrun == '1':
#         iscrashrun = True
#     else:
#         iscrashrun = False
#     optimization = dbgps.get(consts.optimizationname, '0')
#     if optimization == '1':
#         optimization = True
#     else:
#         optimization = False
#     videospath = dbgps.get(consts.videofoldername, default)
#     outputpath = dbgps.get(consts.outputfoldername, default)
#     paramspath = dbgps.get(consts.paramsfilepathname, default)
#
#     gps.append(algoversion)
#     gps.append(algofolder)
#     gps.append(optimization)
#     gps.append(videospath)
#     gps.append(outputpath)
#     gps.append(paramspath)
#     gps.append(crashrunparam)
#
#     return gps