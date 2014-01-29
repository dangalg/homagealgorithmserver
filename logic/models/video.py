__author__ = 'danga_000'


class Video:
    def __init__(self,id,name,pnumofframes,ppath,pffmpeg):
        self.videoid = id
        self.videoname = name
        self.numofframes = pnumofframes
        self.path = ppath
        self.ffmpeg = pffmpeg
