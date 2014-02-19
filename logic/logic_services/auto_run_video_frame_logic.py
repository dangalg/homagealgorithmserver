from data.data_services import auto_run_video_frame_db

__author__ = 'danga_000'


def get_AutoRunVideoFrame_by_cycleidvideoidframeid(cycleid,videoid,frameid):
    return auto_run_video_frame_db.get_AutoRunVideoFrame_by_cycleidvideoidframeid(cycleid,videoid,frameid)


def insert_update_autorunvideoframe(autorunvideoframe):
    if get_AutoRunVideoFrame_by_cycleidvideoidframeid(autorunvideoframe.cycleid,autorunvideoframe.videoid,autorunvideoframe.frameid):
        update_score(autorunvideoframe,autorunvideoframe.score)
    else:
        auto_run_video_frame_db.insert_autorunvideoframe(autorunvideoframe)

def update_score(autorunvideoframe,score):
    auto_run_video_frame_db.update_score(autorunvideoframe,score)

def delete_autorunvideoframe_by_cycleidvideoidframeid(autorunvideoframe):
    auto_run_video_frame_db.delete_autorunvideoframe_by_cycleidvideoidframeid(autorunvideoframe)