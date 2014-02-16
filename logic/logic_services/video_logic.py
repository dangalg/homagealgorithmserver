from data.data_services import video_db
from utils import log
from file import fileIO

__author__ = 'danga_000'

from file import ffmpeg

def get_all_frames_from_video(video):
    frames = {}
    framenum = 0
    for i in range(1,100):
        frame = video.path + '{0:03}'.format(i)
        try:
            framefile = fileIO.get_file_by_name_read(frame)
            frames.update(frame,[video,framefile])
            framenum = framenum + 1
        except IOError:
            log.log_errors("cannot get frames for: " + video.videoid + "name: " +
                           video.videoname + "num of frames: " +
                           video.numofframes + "path: " +
                           video.path + "ffmpeg: " +
                           video.ffmpeg )
    return frames, framenum

def get_all_test_frames_from_video(video,framenum):
    testframes = {}
    testpath = video.path.split('.')[0] + "_GT" + video.path.split('.')
    for i in range(1,framenum):
        frame = testpath + '{0:03}'.format(i)
        try:
            framefile = fileIO.get_file_by_name_read(frame)
            testframes.update(frame,[video,framefile])
        except IOError:
            log.log_errors("cannot get test frames for: " + video.videoid + "name: " +
                           video.videoname + "num of frames: " +
                           video.numofframes + "path: " +
                           testpath + "ffmpeg: " +
                           video.ffmpeg )
    return testframes

def get_all_videos():
    videos = video_db.get_all_videos()
    # videos = {}
    # for video in videosdb:
    #     if video:
    #         try:
    #             videofile = fileIO.get_file_by_name_read(video.path)
    #             videos.update(video.name,[video,videofile])
    #         except IOError:
    #             log.log_errors("cannot get id: " + video.videoid + "name: " +
    #                            video.videoname + "num of frames: " +
    #                            video.numofframes + "path: " +
    #                            video.path + "ffmpeg: " +
    #                            video.ffmpeg )
    return videos

def get_videos_by_search(query):
    videos = video_db.get_videos_by_search(query)
    # videos = {}
    # for video in videosdb:
    #     if video:
    #         try:
    #             videofile = fileIO.get_file_by_name_read(video.path)
    #             videos.update(video.name,[video,videofile])
    #         except IOError:
    #             log.log_errors("cannot get id: " + video.videoid + "name: " +
    #                            video.videoname + "num of frames: " +
    #                            video.numofframes + "path: " +
    #                            video.path + "ffmpeg: " +
    #                            video.ffmpeg )
    return videos

def get_video_by_id(id):
    video =  video_db.delete_video_by_id(id)
    # video = None
    # if videodb:
    #     try:
    #         videofile = fileIO.get_file_by_name_read(videodb.path)
    #         video = {video.name,[videodb,videofile]}
    #     except IOError:
    #         log.log_errors("cannot get id: " + videodb.videoid + "name: " +
    #                        videodb.videoname + "num of frames: " +
    #                        videodb.numofframes + "path: " +
    #                        videodb.path + "ffmpeg: " +
    #                        videodb.ffmpeg )
    return video

def get_video_by_name(name):
    video =  video_db.get_video_by_name(name)
    # video = None
    # if videodb:
    #     try:
    #         videofile = fileIO.get_file_by_name_read(videodb.path)
    #         video = {video.name,[videodb,videofile]}
    #     except IOError:
    #         log.log_errors("cannot get id: " + videodb.videoid + "name: " +
    #                        videodb.videoname + "num of frames: " +
    #                        videodb.numofframes + "path: " +
    #                        videodb.path + "ffmpeg: " +
    #                        videodb.ffmpeg )
    return video

def ffmpeg_on_video(video):
    if video.ffmpeg == 0:
        try:
            ffmpeg.ffmpeg_on_file(video.path)
            video.ffmpeg = 1
            update_video_by_id(video.videoid,video)
        except IOError:
            log.log_errors("cannot get id: " + str(video.videoid) + "name: " +
                           video.videoname + "num of frames: " +
                           str(video.numofframes) + "path: " +
                           video.path + "ffmpeg: " + str(video.ffmpeg) )



def insert_video(video):
    video_db.insert_video(video)

def update_video_by_id(id,video):
    video_db.update_video_by_id(id,video)

def delete_video_by_id(id):
    video_db.delete_video_by_id(id)