__author__ = 'danga_000'
from data import db

#
# VideoID
# VideoName
# number of Frames
# path
# FFMPEG

class Video:
    def __init__(self,id,name,pnumofframes,ppath,pffmpeg):
        self.videoid = id
        self.videoname = name
        self.numofframes = pnumofframes
        self.path = ppath
        self.ffmpeg = pffmpeg



def get_videos_by_search(query):
    vids = []
    query = "SELECT * FROM Videos WHERE video_name LIKE '%{0}%'".format(query)
    cursor = db.get_cursor_from_query(query)
    general_params = cursor.fetchall()
    for row in general_params:
        vid = Video(row[0],row[1],row[2],row[3],row[4])
        vids.append(vid)
    return vids

def get_video_by_id(id):
    query = "SELECT * FROM Videos WHERE video_id = '{0}'".format(id)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    vid = Video(row[0],row[1],row[2],row[3],row[4])
    return vid

def get_video_by_name(name):
    query = "SELECT * FROM Videos WHERE video_name = '{0}'".format(name)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    vid = Video(row[0],row[1],row[2],row[3],row[4])
    return vid
