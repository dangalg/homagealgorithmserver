from algorithm.compare import run_compare
from logic.logic_services.video import get_all_videos

__author__ = 'danga_000'

def run_cycle():
    # set params

    avgscore = 0
    # run cycle on all videos:
    videos = get_all_videos()
    numofvideos = len(videos)
    score = 0
    for video in videos:
        autovideo = run_compare(video)
        score = score + autovideo.averagescore
    avgscore = score / numofvideos
    # create auto_run with params

    # run ffmpeg on all videos

    # run compare on all videos

    # save all videos average in auto_run