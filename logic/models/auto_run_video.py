from data.datamodels import auto_run_video_db

__author__ = 'danga_000'


class AutoRunVideo:
    def __init__(self,pcycleid,pvideoid,paveragescore,pexception):
        self.cycleid = pcycleid
        self.videoid = pvideoid
        self.averagescore = paveragescore
        self.exception = pexception

def get_AutoRunVideo_by_cycleidvideoid(cycleid,videoid):
    return auto_run_video_db.get_AutoRunVideo_by_cycleidvideoid(cycleid,videoid)


def insert_autorunvideo(autorunvideo):
    auto_run_video_db.insert_autorunvideo(autorunvideo)

def update_score(autorunvideo,averagescore,exception):
    auto_run_video_db.update_score(autorunvideo,averagescore,exception)

def delete_autorunvideo_by_cycleidvideoid(autorunvideo):
    auto_run_video_db.delete_autorunvideo_by_cycleidvideoid(autorunvideo)