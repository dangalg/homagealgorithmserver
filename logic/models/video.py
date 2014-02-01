from data.datamodels import video_db
from utils import log
from file import fileIO

__author__ = 'danga_000'


class Video:
    def __init__(self,id,name,pnumofframes,ppath,pffmpeg):
        self.videoid = id
        self.videoname = name
        self.numofframes = pnumofframes
        self.path = ppath
        self.ffmpeg = pffmpeg


def get_videos_by_search(query):
    videosdb = video_db.get_videos_by_search(query)
    videos = {}
    for video in videosdb:
        if video:
            try:
                videofile = fileIO.get_file_by_name_read(video.path)
                videos.update(video.name,[video,videofile])
            except IOError:
                log.log_errors("cannot get id: " + video.videoid + "name: " +
                               video.videoname + "num of frames: " +
                               video.numofframes + "path: " +
                               video.path + "ffmpeg: " +
                               video.ffmpeg )
    return videos

def get_video_by_id(id):
    videodb =  video_db.delete_video_by_id(id)
    video = None
    if videodb:
        try:
            videofile = fileIO.get_file_by_name_read(videodb.path)
            video = {video.name,[videodb,videofile]}
        except IOError:
            log.log_errors("cannot get id: " + videodb.videoid + "name: " +
                           videodb.videoname + "num of frames: " +
                           videodb.numofframes + "path: " +
                           videodb.path + "ffmpeg: " +
                           videodb.ffmpeg )
    return video

def get_video_by_name(name):
    videodb =  video_db.get_video_by_name(name)
    video = None
    if videodb:
        try:
            videofile = fileIO.get_file_by_name_read(videodb.path)
            video = {video.name,[videodb,videofile]}
        except IOError:
            log.log_errors("cannot get id: " + videodb.videoid + "name: " +
                           videodb.videoname + "num of frames: " +
                           videodb.numofframes + "path: " +
                           videodb.path + "ffmpeg: " +
                           videodb.ffmpeg )
    return video

def insert_video(video):
    video_db.insert_video(video)

def update_video_by_id(id,video):
    video_db.update_video_by_id(id,video)

def delete_video_by_id(id):
    video_db.delete_video_by_id(id)