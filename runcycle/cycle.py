import datetime
import itertools
import os
from tkinter import END
from algorithm.algorithm import create_params_output_path

from algorithm.prepare_algorithm import run_algorithm_then_compare
from file import fileIO
from logic.logic_services import auto_run_video_logic
from logic.logic_services import auto_run_logic
from logic.logic_services.general_param_logic import insert_update_general_param
from logic.logic_services.parameter_logic import insert_param
from logic.logic_services.video_logic import insert_update_videos_from_path
from models.autorun import AutoRun
from logic.logic_services import general_param_logic
from models.generalparam import GeneralParam
from models.parameter import Parameter
from utils import log
from utils import consts


__author__ = 'danga_000'

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


def set_user_info(optimize,algoversion,mainfolder):
    #set Algorithm output and version
    print("Saving folders to database...")
    gps = []
    gpalgoversion = GeneralParam('AlgorithmVersion', str(algoversion))
    gpalgofolder = GeneralParam('AlgorithmFolder', str(mainfolder + '/' + consts.algorithem + '/'))
    optimization = False
    if optimize == '1':
        optimization = True
    algorunoptimization = GeneralParam('RunOptimization', optimization)
    videofolder = GeneralParam('VideoFolder', str(mainfolder + '/' + consts.videos + '/'))
    outputfolder = GeneralParam('OutputFolder', str(mainfolder + '/' + consts.output + '/'))
    paramsfolder = GeneralParam('ParamsFolder', str(mainfolder + '/' + consts.paramsxml))
    insert_update_general_param(gpalgofolder)
    insert_update_general_param(gpalgoversion)
    insert_update_general_param(algorunoptimization)
    insert_update_general_param(videofolder)
    insert_update_general_param(outputfolder)
    insert_update_general_param(paramsfolder)
    gps.append(gpalgoversion)
    gps.append(gpalgofolder)
    gps.append(algorunoptimization)
    gps.append(videofolder)
    gps.append(outputfolder)
    gps.append(paramsfolder)
    createfolders(gps)
    return gps

def getParamsFromFile(gps, cycleid):
    #  get params from path to params
    parameters = []
    with open(gps[consts.paramsfilepath].val,'r') as f:
        for x in f:
            row = x.split(',')
            if len(row) == 5:
                param = Parameter(cycleid, gps[consts.algoversion].val,row[0],row[1],row[2],row[3],row[4].replace('\n',''))
                parameters.append(param)
                insert_param(param)
    return parameters



def deleteContent(fName):
    with open(fName, "w"):
        pass


def get_starting_general_params():
    dbgps = general_param_logic.get_general_params()
    gps = []
    default = 'Set Folder Please'
    algoversion = dbgps.get(consts.algoversionname, default)
    algofolder = dbgps.get(consts.algofoldername, default)
    optimization = dbgps.get(consts.optimizationname, '0')
    if optimization == '1':
        optimization = True
    else:
        optimization = False
    videospath = dbgps.get(consts.videofoldername, default)
    outputpath = dbgps.get(consts.outputfoldername, default)
    paramspath = dbgps.get(consts.paramsfilepathname, default)

    gps.append(algoversion)
    gps.append(algofolder)
    gps.append(optimization)
    gps.append(videospath)
    gps.append(outputpath)
    gps.append(paramspath)

    return gps


def save_avgscore_to_report(gps, avgscore, cycleid):
    path = os.path.abspath(gps[consts.outputfolder].val + gps[consts.algoversion].val + "/" + str(cycleid) + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    file = fileIO.get_file_by_name_write(path + "\\" + "cycle-" + str(cycleid) + "-score.txt")
    file.write(str(avgscore))


def createfolders(gps):
    path = gps[consts.algofolder].val
    if not os.path.exists(path):
        os.makedirs(path)
    path = gps[consts.videofolder].val
    if not os.path.exists(path):
        os.makedirs(path)
    path = gps[consts.outputfolder].val
    if not os.path.exists(path):
        os.makedirs(path)



def run_video_cycle(gps, cycleid, numofvideos,permutations, startdate, videos):
    videocount = numofvideos
    i=2
    avgscore = 0
    for video in videos:
        i = i+1
        print("Testing " + video.videoname)
        # run ffmpeg on video and run_compare
        try:
            #     ffmpeg_on_video(video)
            autovideo = run_algorithm_then_compare(gps, cycleid, video)
            if autovideo.averagescore != 0:
                avgscore = avgscore + autovideo.averagescore
                print("Score: " + str(autovideo.averagescore))
            else:
                videocount -= 1
        except IOError:
            log.log_information(IOError)
            videocount -= 1
            print("Error in video: " + video.videoname)
    # Save average score
    if videocount != 0:
        avgscore = avgscore / videocount
    else:
        avgscore = 0
    # create auto_run with params



    stringpermutation = ''
    for permutation in permutations:
        stringpermutation += permutation + ','
    stringpermutation = stringpermutation[:-1]
    ar = AutoRun(cycleid, gps[consts.algoversion].val, stringpermutation, startdate, datetime.datetime.now(), avgscore)
    # Save autorun info
    auto_run_logic.insert_autorun(ar)
    save_avgscore_to_report(gps, avgscore, cycleid)
    print("**** Finished Cycle " + str(cycleid) + " Score: " + str(avgscore) + " ****")


def run_cycle(optimize,algoversion,mainfolder):
    # get new cycle_id
    cycleid = auto_run_video_logic.get_new_cycle_id()
    print("Starting Run Cycle " + str(cycleid))
    print("Setting params...")
    gps = set_user_info(optimize,algoversion,mainfolder)
    # get existing videos automatically from their folder and aws and insert to database if needed
    videos = insert_update_videos_from_path(gps[consts.videofolder].val)
    numofvideos = len(videos)
    permutationparams = getParamsFromFile(gps, cycleid)
    paramlists = get_params_list(gps[consts.optimization].val,permutationparams)
    if gps[consts.optimization].val:
        permutationlist = list(itertools.product(*paramlists))
    else:
        permutationlist = paramlists
    # ----cycle through params------
    # Empty params file and refill it
    paramsfile = create_params_output_path(gps, cycleid) + '/' + consts.paramsxml

    for i in range(0, len(permutationlist)):
        # fix params file
        deleteContent(paramsfile)
        with open(paramsfile, "a") as myfile:
            myfile.write("<UniformBackgroundPrm>")
        for j in range(0, len(permutationparams)):
            with open(paramsfile, "a") as myfile:
                myfile.write('<' + permutationparams[j].name +'>' + str(permutationlist[i][j]) + '</' + permutationparams[j].name + '>')
        with open(paramsfile, "a") as myfile:
            myfile.write("</UniformBackgroundPrm>")
        startdate= datetime.datetime.now()
        # run cycle on all videos:
        score = 0
        print("running " + str(i) + " permutation: " + str(permutationlist[i]))
        run_video_cycle(gps, cycleid, numofvideos, permutationlist[i], startdate, videos)
        cycleid += 1
        paramsfile = create_params_output_path(gps, cycleid) + '/' + consts.paramsxml

    print("***********FINISHED**************")
