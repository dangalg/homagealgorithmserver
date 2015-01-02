from data.data_services import crash_run_video_db

__author__ = 'danga_000'

def get_crashrunvideo_by_cycleidvideoid(cycleid,videoid):
    return crash_run_video_db.get_crashrunvideo_by_cycleidvideoid(cycleid,videoid)

def insert_crashrunvideo(crashrunvideo):
        crash_run_video_db.insert_crash_run_video(crashrunvideo)

def update_crashrunvideo(crashrunvideo):
    crash_run_video_db.update_crashrunvideo(crashrunvideo)