import os
from data import aws_helper
from data.data_services import video_db
from file.fileIO import list_videos_by_path, list_frames_by_path
from models.video import Video
from utils import log
from utils import consts

__author__ = 'danga_000'

from file import ffmpeg

# def log_video_error(message, video=None):
#     if video:
#         log.log_information(message + str(video.videoid) + "name: " +
#                            video.videoname + "num of frames: " +
#                            str(video.numofframes) + "path: " +
#                            video.path + "ffmpeg: " +
#                            str(video.ffmpeg) )
#     else:
#         log.log_information(message + " Video info not available")

def get_new_video_id():
    topid = video_db.get_top_video_id()
    newid = 1
    if topid:
        newid = topid + 1
    return newid

def get_all_frames_from_video(video):
    frames = []
    path = get_frame_path(video)
    if os.path.exists(path):
        frames = list_frames_by_path(path)
        # for i in range(1,video.numofframes + 1):
        #     frame = get_frame_path(video) + "/" + "image" + "-" + '{0:04}'.format(i) + ".jpg"
        #     if os.path.exists(frame):
        #         frames.append(frame)
    return frames

# def get_gt_file(video):
#     GTpath = get_GT_path(video)
#     if os.path.exists(GTpath):
#         return get_plf_file(GTpath)
#         testframes = get_plf_file(GTpath)
#         # testpath = get_GT_path(video) + "/" + "image" + "-"
#         # for i in range(0,video.numofframes):
#         #     frame = testpath + '{0:02}'.format(i) + ".bmp"
#         #     if os.path.exists(frame):
#         #         testframes.append(frame)
#     return testframes

# def get_all_gt_files_from_video(video):
#     testframes = []
#     GTpath = get_GT_path(video)
#     if os.path.exists(GTpath):
#         testframes = get_algo_plf_file(GTpath)
#         # testpath = get_GT_path(video) + "/" + "image" + "-"
#         # for i in range(0,video.numofframes):
#         #     frame = testpath + '{0:02}'.format(i) + ".bmp"
#         #     if os.path.exists(frame):
#         #         testframes.append(frame)
#     return testframes

def escape_backslash(name):
    # name = os.path.abspath(name)
    return name

def get_all_videos():
    videos = video_db.get_all_videos()
    for video in videos:
        video.path = escape_backslash(video.path)
    return videos

def get_videos_by_search(query):
    videos = video_db.get_videos_by_search(query)
    for video in videos:
        video.path = escape_backslash(video.path)
    return videos

def get_video_by_id(id):
    video =  video_db.delete_video_by_id(id)
    video.path = escape_backslash(video.path)
    return video

def get_video_by_name(name):
    video =  video_db.get_video_by_name(name)
    if video:
        video.path = escape_backslash(video.path)
        return video

# def ffmpeg_on_video(video):
#     if video.ffmpeg == 0:
#         try:
#             ffmpeg.ffmpeg_on_path(video.path)
#             video.ffmpeg = 1
#             update_ffmpeg(video)
#         except IOError:
#             log_video_error("ffmpeg_on_video error: ", video)

def update_ffmpeg(video):
    video.ffmpeg = 1
    video_db.update_video_by_id(video.videoid,video)

def get_framnum_from_path(video):
    frames = list_frames_by_path(get_frame_path(video)) # Gets jpg files!
    return len(frames)

def get_frame_path(video):
    return video.path + "/" + "Frames" #video.videoname.split('.')[0]

def get_GT_path(video):
    return video.path #video.videoname.split('.')[0]

def insert_update_videos_from_path(gps):
    videos = comparevideosfroms3tolocalandadjust(gps)
    newid = get_new_video_id()
    vid = None
    videosinfolder = []
    for v in videos:
        try:
            updvid = get_video_by_name(v)
            videosfolder = gps[consts.videofoldername].val
            if gps[consts.crashrunname].val:
                videosfolder = gps[consts.crashrunvideofoldername].val
            vid = Video(newid, v, 0 , videosfolder + v, 0)
            framenum = get_framnum_from_path(vid)
            vid.numofframes = framenum # Frames must be in a folder with the same name as the video
            # Example: videoname path = c:\test.avi frames path = c:\test\
            # Video name is unique

            if not updvid:
                video_db.insert_video(vid)
                newid += 1
            else:
                video_db.update_video_by_id(updvid.videoid,vid)
                vid.videoid = updvid.videoid
            videosinfolder.append(vid)
        except IOError as e:
            log.log_information("insert_update_videos_from_path error in video: " + vid.videoname + " " + str(e.args).replace("'",""))
    return videosinfolder

def comparevideosfroms3tolocalandadjust(gps):

    if gps[consts.crashrunname].val:
        localvideos = list_videos_by_path(gps[consts.crashrunvideofoldername].val)
    else:
        localvideos = list_videos_by_path(gps[consts.videofoldername].val)
    # create path to video folder without video folder name because it is added automatically
    directory = gps[consts.mainfoldername].val
    awsvideofolder = consts.awsvideos
    if gps[consts.crashrunname].val:
        awsvideofolder = consts.awscrashrunvideos
    s3videos = aws_helper.listfolderfroms3('homage-automation', awsvideofolder)

    for s3vid in s3videos:
        videofound = False
        for vid in localvideos:
            if vid == s3vid:
                videofound = True
        if not videofound or any(s3vid in s for s in gps[consts.remakelistname].val):
            print("Downloading: " + str(s3vid))
            aws_helper.downloadfolderfroms3('homage-automation', awsvideofolder + s3vid, directory + '/')
    return s3videos  #localvideos

# def insert_update_video(video):
#     newid = get_new_video_id()
#     updvid = get_video_by_name(video.videoname)
#     try:
#         framenum = get_framnum_from_path(video) # Frames must be in a folder with the same name as the video
#         video.videoid = newid
#         video.numofframes = framenum
#         if not updvid:
#             video_db.insert_video(video)
#         else:
#             video_db.update_video_by_id(updvid.videoid,video)
#     except IOError:
#             log_video_error("insert_update_videos_from_path error in video named {0}: ".format(video.videoname), video)
#
# def delete_video_by_id(id):
#     video_db.delete_video_by_id(id)