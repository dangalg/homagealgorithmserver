from data.data_services import auto_run_video_frame_db

__author__ = 'danga_000'


# def get_AutoRunVideoFrame_by_cycleidvideoidframeid(cycleid,videoid,frameid):
#     return auto_run_video_frame_db.get_AutoRunVideoFrame_by_cycleidvideoidframeid(cycleid,videoid,frameid)


def insert_autorunvideoframe(autorunvideoframe):
        auto_run_video_frame_db.insert_autorunvideoframe(autorunvideoframe)

# def update_score(autorunvideoframe,score):
#     auto_run_video_frame_db.update_score(autorunvideoframe,score)

def delete_autorunvideoframes_by_cycleidvideoid(cycleid, videoid):
    auto_run_video_frame_db.delete_autorunvideoframes_by_cycleidvideoid(cycleid, videoid)


def get_new_autorunvideoframe_id():
    topid = auto_run_video_frame_db.get_top_autorunvideoframe_id()
    newid = 1
    if topid:
        newid = topid + 1
    return newid