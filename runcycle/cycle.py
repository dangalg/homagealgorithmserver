import datetime
import itertools
import os
from tkinter import END
from algorithm.algorithm import create_params_output_path

from algorithm.prepare_algorithm import run_algorithm_then_compare
from file import fileIO
from logic.logic_services import auto_run_logic
from logic.logic_services.general_param_logic import insert_update_general_param
from logic.logic_services.parameter_logic import insert_param
from logic.logic_services.video_logic import insert_update_videos_from_path
from models.autorun import AutoRun
from logic.logic_services import general_param_logic
from models.generalparam import GeneralParam
from models.parameter import Parameter
from utils import log


__author__ = 'danga_000'

# range of floats
def frange(min, max, jump):
    paramlist = []
    while min < max:
        paramlist.append(min)
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
            paramlist = frange(param.min, param.max+1, param.change)
            paramlists.append(paramlist)
        else:
            paramtuple = paramtuple + (param.default,)
    if optimize:
        return paramlists
    else:
        return [paramtuple]


def set_user_info(app, optimize,algoversion,algofolder,videofolder, paramspath, cycleid):
    #set Algorithm output and version
    app.lbreport.insert(END,"Saving folders to database...")
    gpalgoversion = GeneralParam('AlgorithmVersion', str(algoversion))
    gpalgofolder = GeneralParam('AlgorithmFolder', str(algofolder))
    algorunoptimization = GeneralParam('RunOptimization', str(optimize))
    videofolder = GeneralParam('VideoFolder', str(videofolder))
    paramsfolder = GeneralParam('ParamsFolder', str(paramspath))
    insert_update_general_param(gpalgofolder)
    insert_update_general_param(gpalgoversion)
    insert_update_general_param(algorunoptimization)
    insert_update_general_param(videofolder)
    insert_update_general_param(paramsfolder)
    # Remove all params
    # TODO put param in database with cycleid for later reference
    # dbparams = get_params_by_algo_version(algoversion)
    # for dbparam in dbparams:
    #     delete_param_by_name(algoversion, dbparam.name)
    # Insert params from file
    app.lbreport.insert(END,"Saving params to database...")
    return getParamsFromFile(cycleid, algoversion, paramspath)

def getParamsFromFile(cycleid, algoversion, paramspath):
    #  get params from path to params
    parameters = []
    with open(paramspath,'r') as f:
        for x in f:
            row = x.split(',')
            if len(row) == 5:
                param = Parameter(cycleid, algoversion,row[0],row[1],row[2],row[3],row[4].replace('\n',''))
                parameters.append(param)
                insert_param(param)
    return parameters



def deleteContent(fName):
    with open(fName, "w"):
        pass


def get_general_params():
    gps = general_param_logic.get_general_params()
    default = 'Set Folder Please'
    algoversion = gps.get('AlgorithmVersion', default)
    algofolder = gps.get('AlgorithmFolder', default)
    algorunoptimization = gps.get('RunOptimization', '0')
    if algorunoptimization == '1':
        algorunoptimization = True
    else:
        algorunoptimization = False
    videospath = gps.get('VideoFolder', default)
    paramspath = gps.get('ParamsFolder', default)
    return algoversion, algofolder, algorunoptimization, videospath, paramspath


def save_avgscore_to_report(algoversion, avgscore, cycleid, videospath):
    path = os.path.abspath(videospath + "/" + algoversion + "/" + str(cycleid) + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    file = fileIO.get_file_by_name_write(path + "\\" + "cycle-" + str(cycleid) + "-score.txt")
    file.write(str(avgscore))


def run_video_cycle(app, algoversion, algofolder, cycleid, numofvideos,permutations, params, score, startdate, videos, videospath):
    videocount = numofvideos
    i=2
    avgscore = 0
    for video in videos:
        i = i+1
        app.lblstatus['text'] = "Testing " + video.videoname
        app.lbreport.insert(END, "Testing " + video.videoname)
        # run ffmpeg on video and run_compare
        try:
            #     ffmpeg_on_video(video)
            autovideo = run_algorithm_then_compare(cycleid, video,algofolder,algoversion, params)
            if autovideo.averagescore != 0:
                avgscore = avgscore + autovideo.averagescore
                app.lbreport.insert(END,"Score: " + str(autovideo.averagescore))
            else:
                videocount -= 1
        except IOError:
            log.log_errors(IOError)
            videocount -= 1
            app.lbreport.insert(END,"Error in video: " + video.videoname)
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
    ar = AutoRun(cycleid, algoversion, stringpermutation, startdate, datetime.datetime.now(), avgscore)
    # Save autorun info
    auto_run_logic.insert_autorun(ar)
    save_avgscore_to_report(algoversion, avgscore, cycleid, videospath)
    app.lbreport.insert(END,"**** Finished Cycle " + str(cycleid) + " Score: " + str(avgscore) + " ****")


def run_cycle(app, optimize,algoversion,algofolder,videofolder,paramspath):
    app.lblstatus['text'] = "Setting params..."

    # get new cycle_id
    cycleid = auto_run_logic.get_new_cycle_id()
    app.lbreport.insert(END, "Starting Run Cycle " + str(cycleid))
    app.lbreport.insert(END,"Setting params...")
    pemutationparams = set_user_info(app,optimize,algoversion,algofolder,videofolder,paramspath,cycleid)
    # Get general_params
    algoversion,algofolder, algorunoptimization, videospath, paramspath = get_general_params()
    # get existing videos automatically from their folder and insert to database if needed
    videos = insert_update_videos_from_path(videospath)
    numofvideos = len(videos)
    paramlists = get_params_list(algorunoptimization,pemutationparams)
    if algorunoptimization:
        permutationlist = list(itertools.product(*paramlists))
    else:
        permutationlist = paramlists
    # ----cycle through params------
    # Empty params file and refill it
    paramsfile = create_params_output_path(algofolder, cycleid, algoversion) + '/params.xml'

    for i in range(0, len(permutationlist)):
        # fix params file
        deleteContent(paramsfile)
        with open(paramsfile, "a") as myfile:
            myfile.write("<UniformBackgroundPrm>")
        for j in range(0, len(pemutationparams)):
            with open(paramsfile, "a") as myfile:
                myfile.write('<' + pemutationparams[j].name +'>' + str(permutationlist[i][j]) + '</' + pemutationparams[j].name + '>')
        with open(paramsfile, "a") as myfile:
            myfile.write("</UniformBackgroundPrm>")
        startdate= datetime.datetime.now()
        # run cycle on all videos:
        score = 0
        app.lbreport.insert(END,"running " + str(i) + " permutation: " + str(permutationlist[i]))
        run_video_cycle(app, algoversion,algofolder, cycleid, numofvideos,permutationlist[i], pemutationparams, score, startdate, videos, videospath)
        cycleid += 1
        paramsfile = create_params_output_path(algofolder, cycleid, algoversion) + '/params.xml'

    app.lbreport.insert(END,"***********FINISHED**************")
