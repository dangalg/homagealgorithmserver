__author__ = 'danga_000'
import MySQLdb
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



def get_videos_by_name(query):
    vids = []
    query = "SELECT * FROM Videos WHERE "
    cursor = db.get_cursor_from_query(query)
    general_params = cursor.fetchall()
    for row in general_params:
        gp = General_Param(row[0],row[1])
        gps.append(gp)
    return vids
