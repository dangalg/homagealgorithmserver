from data.datamodels import auto_run_video_frame_db

__author__ = 'danga_000'


class AutoRunVideoFrame:
    def __init__(self,pcycleid,pvideoid,pframeid,score):
        self.cycleid = pcycleid
        self.videoid = pvideoid
        self.frameid = pframeid
        self.score = score

def get_AutoRunVideoFrame_by_cycleidvideoidframeid(cycleid,videoid,frameid):
    return auto_run_video_frame_db.get_AutoRunVideoFrame_by_cycleidvideoidframeid(cycleid,videoid,frameid)


def insert_autorunvideoframe(autorunvideoframe):
    auto_run_video_frame_db.insert_autorunvideoframe(autorunvideoframe)

def update_score(autorunvideoframe,score):
    auto_run_video_frame_db.update_score(autorunvideoframe,score)

def delete_autorunvideoframe_by_cycleidvideoidframeid(autorunvideoframe):
    auto_run_video_frame_db.delete_autorunvideoframe_by_cycleidvideoidframeid(autorunvideoframe)