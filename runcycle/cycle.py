import datetime
import itertools
import os
from algorithm.algorithm import run_algorithm, create_algorithm_output_path, create_params_output_path

from algorithm.prepare_algorithm import run_algorithm_then_compare
from file import fileIO
from logic.logic_services import auto_run_logic
from logic.logic_services.general_param_logic import insert_update_general_param
from logic.logic_services.parameter_logic import insert_update_param_by_name, get_all_params, delete_param_by_name, \
    get_params_by_algo_version
from logic.logic_services.video_logic import get_all_videos, insert_update_videos_from_path
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


def get_params_list(optimize,algoversion):
    paramlists = []
    paramtuple = ()
    # Get params from database to list
    paramsdb = get_params_by_algo_version(algoversion)
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


def set_user_info(optimize,algoversion,algofolder,algooutputfolder,videofolder,params):
    #set Algorithm output and version
    gpalgooutput = GeneralParam('AlgorithmOutput', str(algooutputfolder))
    gpalgoversion = GeneralParam('AlgorithmVersion', str(algoversion))
    gpalgofolder = GeneralParam('AlgorithmFolder', str(algofolder))
    algorunoptimization = GeneralParam('RunOptimization', str(optimize))
    videofolder = GeneralParam('VideoFolder', str(videofolder))
    insert_update_general_param(gpalgooutput)
    insert_update_general_param(gpalgofolder)
    insert_update_general_param(gpalgoversion)
    insert_update_general_param(algorunoptimization)
    insert_update_general_param(videofolder)
    # Remove all params
    dbparams = get_params_by_algo_version(algoversion)
    for dbparam in dbparams:
        delete_param_by_name(algoversion, dbparam.name)
    # Insert params from user
    for param in params:
        insert_update_param_by_name(algoversion, param.name, param)


def deleteContent(fName):
    with open(fName, "w"):
        pass


def get_general_params():
    gps = general_param_logic.get_general_params()
    algooutput = gps['AlgorithmOutput']
    algoversion = gps['AlgorithmVersion']
    algofolder = gps['AlgorithmFolder']
    if gps['RunOptimization'] == '1':
        algorunoptimization = True
    else:
        algorunoptimization = False
    videospath = gps['VideoFolder']
    return algooutput, algoversion, algofolder, algorunoptimization, videospath


def save_avgscore_to_report(algooutput, algoversion, avgscore, cycleid, videospath):
    path = os.path.abspath(algooutput + "/" + algoversion + "/" + str(cycleid) + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    file = fileIO.get_file_by_name_write(path + "\\" + "cycle-" + str(cycleid) + "-score.txt")
    file.write(str(avgscore))


def run_video_cycle(app, algooutput, algoversion, algofolder, cycleid, numofvideos,permutations, params, score, startdate, videos, videospath):
    videocount = numofvideos
    i=2
    avgscore = 0
    for video in videos:
        i = i+1
        app.lblstatus['text'] = "Testing " + video.videoname
        app.lbreport.insert(2, "Testing " + video.videoname)
        # run ffmpeg on video and run_compare
        try:
            # if video.ffmpeg == 0: #TODO make ffmpeg work if needed
            #     ffmpeg_on_video(video)
            autovideo = run_algorithm_then_compare(cycleid, video,algooutput,algofolder,algoversion, params)
            if autovideo.averagescore != 0:
                avgscore = avgscore + autovideo.averagescore
                app.lbreport.insert(i,"Score: " + str(autovideo.averagescore))
            else:
                videocount -= 1
        except IOError:
            log.log_errors("cannot get id: " + str(video.videoid) + "name: " +
                           video.videoname + "num of frames: " +
                           str(video.numofframes) + "path: " +
                           video.path + "ffmpeg: " +
                           str(video.ffmpeg))
            videocount -= 1
            app.lbreport.insert(video.videoname,"Error in video: " + video.videoname)
    # Save average score
    if videocount != 0:
        avgscore = avgscore / videocount
    else:
        avgscore = 0
    # create auto_run with params
    app.lbreport.insert(cycleid,"Cycle " + str(cycleid) + " Score: " + str(avgscore))

    ar = AutoRun(cycleid, algoversion, permutations, startdate, datetime.datetime.now(), avgscore)
    # Save autorun info
    auto_run_logic.insert_update_autorun(ar)
    save_avgscore_to_report(algooutput, algoversion, avgscore, cycleid, videospath)


def run_cycle(app, optimize,algoversion,algofolder,algooutputfolder,videofolder,params):
    app.lblstatus['text'] = "Setting params..."
    app.lbreport.insert(2,"Setting params...")
    # get new cycle_id
    cycleid = auto_run_logic.get_new_cycle_id()
    set_user_info(optimize,algoversion,algofolder,algooutputfolder,videofolder,params)
    # Get general_params
    algooutput, algoversion,algofolder, algorunoptimization, videospath = get_general_params()
    # get existing videos automatically from their folder and insert to database if needed
    videos = insert_update_videos_from_path(videospath)
    numofvideos = len(videos)
    paramlists = get_params_list(algorunoptimization,algoversion)
    if algorunoptimization:
        permutationlist = list(itertools.product(*paramlists))
    else:
        permutationlist = paramlists
    # ----cycle through params------
    # Empty params file and refill it
    paramsfile = create_params_output_path(cycleid, algooutput, algoversion) + '/params.xml'
    for i in range(0, len(permutationlist)):
        # fix params file
        deleteContent(paramsfile)
        with open(paramsfile, "a") as myfile:
            myfile.write("<UniformBackgroundPrm>\n")
        for j in range(0, len(params)):
            with open(paramsfile, "a") as myfile:
                myfile.write('<' + params[j].name +'>' + str(permutationlist[i][j]) + '</' + params[j].name + '>\n')
        with open(paramsfile, "a") as myfile:
            myfile.write("</UniformBackgroundPrm>")
        startdate= datetime.datetime.now()
        # run cycle on all videos:
        score = 0
        run_video_cycle(app, algooutput, algoversion,algofolder, cycleid, numofvideos,permutationlist[i], params, score, startdate, videos, videospath)
        paramsfile = create_params_output_path(cycleid, algooutput, algoversion) + '/params.xml'
        cycleid += 1
