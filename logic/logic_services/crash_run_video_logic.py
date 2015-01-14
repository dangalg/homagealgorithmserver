from data.data_services import crash_run_video_db

__author__ = 'danga_000'

def get_crashrunvideo_by_cycleidvideoid(cycleid,videoid):
    return crash_run_video_db.get_crashrunvideo_by_cycleidvideoid(cycleid,videoid)

def insert_crashrunvideo(crashrunvideo):
        crash_run_video_db.insert_crash_run_video(crashrunvideo)

def update_crashrunvideo(crashrunvideo):
    crash_run_video_db.update_crashrunvideo(crashrunvideo)


def get_new_crashrunvideo_id():
    topid = crash_run_video_db.get_top_crashrunvideo_id()
    newid = 1
    if topid:
        newid = topid + 1
    return newid