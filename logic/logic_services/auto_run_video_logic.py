from data.data_services import auto_run_video_db

__author__ = 'danga_000'



def get_autorunvideo_by_cycleidvideoid(cycleid,videoid):
    return auto_run_video_db.get_AutoRunVideo_by_cycleidvideoid(cycleid,videoid)


def insert_autorunvideo(autorunvideo):
        auto_run_video_db.insert_autorunvideo(autorunvideo)

def update_autorunvideo(autorunvideo):
    auto_run_video_db.update_autorunvideo(autorunvideo)

def delete_autorunvideo_by_cycleidvideoid(autorunvideo):
    auto_run_video_db.delete_autorunvideo_by_cycleidvideoid(autorunvideo)


def get_new_autorunvideo_id():
    topid = auto_run_video_db.get_top_autorunvideo_id()
    newid = 1
    if topid:
        newid = topid + 1
    return newid
