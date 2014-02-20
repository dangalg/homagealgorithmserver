from data.data_services import auto_run_video_db

__author__ = 'danga_000'



def get_AutoRunVideo_by_cycleidvideoid(cycleid,videoid):
    return auto_run_video_db.get_AutoRunVideo_by_cycleidvideoid(cycleid,videoid)


def insert_update_autorunvideo(autorunvideo):
    if get_AutoRunVideo_by_cycleidvideoid(autorunvideo.cycleid,autorunvideo.videoid):
        update_score(autorunvideo,autorunvideo.averagescore,autorunvideo.avexception)
    else:
        auto_run_video_db.insert_autorunvideo(autorunvideo)

def update_score(autorunvideo,averagescore,avexception):
    auto_run_video_db.update_score(autorunvideo,averagescore,avexception)

def delete_autorunvideo_by_cycleidvideoid(autorunvideo):
    auto_run_video_db.delete_autorunvideo_by_cycleidvideoid(autorunvideo)