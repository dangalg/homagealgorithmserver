import datetime
from algorithm.compare import run_compare
from file import fileIO
from file.ffmpeg import ffmpeg_on_path
from logic.logic_services import auto_run_logic
from logic.logic_services.general_param_logic import update_general_param_val_by_name
from logic.logic_services.parameter_logic import insert_update_param_by_name
from logic.logic_services.video_logic import get_all_videos
from models.autorun import AutoRun
from logic.logic_services import general_param_logic
from models.parameter import Parameter
from utils import log

__author__ = 'danga_000'

def run_cycle():
    # get cycle_id
    cycleid = auto_run_logic.get_top_cycle_id() + 1
    #set Algorithm output and version
    algooutput = 'C:\\Video database\\AlgoOutput\\' # TODO get from user
    algoversion = '1.2' # TODO get from user
    algorunoptimization = '1' # TODO get from user
    update_general_param_val_by_name('AlgorithmOutput', algooutput)
    update_general_param_val_by_name('AlgorithmVersion', algoversion)
    update_general_param_val_by_name('RunOptimization', algorunoptimization)
    # set params
    x = Parameter() # TODO get from user
    x.name = 'x'
    x.min = 1
    x.max = 2
    x.change = 1
    x.default = 2
    y = Parameter() # TODO get from user
    y.name = 'y'
    y.min = 2
    y.max = 3
    y.change = 1.5
    y.default = 2
    insert_update_param_by_name('x',x)
    insert_update_param_by_name('y',y)
    # Get general_params
    gps = general_param_logic.get_general_params()
    algooutput = gps['AlgorithmOutput']
    algoversion = gps['AlgorithmVersion']
    algorunoptimization = gps['RunOptimization']
    # Get Params into a list of tuples
    for i in range(x.min,x.max):
        for j in range(y.min,y.max):
            px = i / x.change
            py = j / y.change

            # (ParamMax(x)-ParamMin(x))/ParamChange(x) * ParamMax(y)-ParamMin(y))/ParamChange(y)

            # run parameters on all videos
            # test all params on all videos
            ar = AutoRun()
            ar.cycleid = cycleid
            ar.algoversion = algoversion
            ar.params = (px,py)
            ar.startdate = datetime.datetime.now()
            # run cycle on all videos:
            avgscore = 0
            videos = get_all_videos()
            numofvideos = len(videos)
            score = 0
            for video in videos:
                # run ffmpeg on video and run_compare
                try:
                    ffmpeg_on_path(video.path)
                    autovideo = run_compare(cycleid, video,ar.params)
                    score = score + autovideo.averagescore
                except IOError:
                    log.log_errors("cannot get id: " + video.videoid + "name: " +
                                       video.videoname + "num of frames: " +
                                       video.numofframes + "path: " +
                                       video.path + "ffmpeg: " +
                                       video.ffmpeg )
            avgscore = score / numofvideos
            # create auto_run with params
            ar.enddate = datetime.datetime.now()
            ar.avgscore = avgscore
            # Save autorun info
            auto_run_logic.insert_autorun(ar)