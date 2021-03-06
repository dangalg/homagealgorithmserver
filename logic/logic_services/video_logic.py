import os

from data import aws_helper
from data.data_services import video_db
from file import zippy
from file.fileIO import list_videos_by_path, list_frames_by_path
from models.video import Video
from utils import log
from utils import consts


__author__ = 'danga_000'

# from file import ffmpeg

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
            log.log_information(gps, "insert_update_videos_from_path error in video: " + vid.videoname + " " + str(e.args).replace("'",""))
    return videosinfolder


def comparevideosfroms3tolocalandadjust(gps):

    videofoldername = ''
    if gps[consts.crashrunname].val:
        videofoldername = gps[consts.crashrunvideofoldername].val
    else:
        videofoldername = gps[consts.videofoldername].val


    if gps[consts.crashrunname].val:
        localvideos = list_videos_by_path(gps[consts.crashrunvideofoldername].val)
    else:
        localvideos = list_videos_by_path(gps[consts.videofoldername].val)
    # create path to video folder without video folder name because it is added automatically
    directory = gps[consts.mainfoldername].val
    awsvideofolder = consts.awsvideos
    if gps[consts.crashrunname].val:
        awsvideofolder = consts.awscrashrunvideos
    s3files = aws_helper.listfolderfroms3(consts.awsautomationbucket, awsvideofolder)
    s3videos = []
    # Remove zip files from s3 list
    for s3vid in s3files:
        if ".zip" not in s3vid and 'Videos' not in s3vid:
            s3videos.append(s3vid)

    # check if video is on local computer and if not then download it
    for s3vid in s3videos:
        videofound = False
        for vid in localvideos:
            if vid == s3vid:
                videofound = True
        if not videofound or \
                any(s3vid in s for s in gps[consts.remakelistname].val) or \
                gps[consts.updatedbname].val:
            print("Downloading: " + str(s3vid))
            aws_helper.downloadfolderfroms3(consts.awsautomationbucket, awsvideofolder + s3vid, directory + '/')
            print("Zipping: " + str(s3vid))
            zippy.zip_video_folder(videofoldername + s3vid,
                                   videofoldername + s3vid)
            print("Uploading: " + str(s3vid))
            aws_helper.uploadfiletos3(consts.awsautomationbucket,
                                      awsvideofolder + s3vid + '.zip',
                                      videofoldername + s3vid + '.zip')
    return s3videos  #localvideos


def get_video_by_name(name):
    video =  video_db.get_video_by_name(name)
    if video:
        # video.path = escape_backslash(video.path)
        return video


def get_new_video_id():
    topid = video_db.get_top_video_id()
    newid = 1
    if topid:
        newid = topid + 1
    return newid


def get_framnum_from_path(video):
    if not os.path.exists(get_frame_path(video)):
        return 0
    frames = list_frames_by_path(get_frame_path(video)) # Gets jpg files!
    return len(frames)


def get_frame_path(video):
    return video.path + "/" + "Frames" #video.videoname.split('.')[0]