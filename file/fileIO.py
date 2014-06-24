import os
import os.path

__author__ = 'danga_000'

def get_file_by_name_write(filename):

    return open(filename,'a+')

def get_file_by_name_read(filename):
    return open(filename,'a+')

def list_videos_by_path(path):
    videos = []
    videos = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    # for file in os.listdir(os.path.abspath(path)):
    #     if file.endswith(".mp4"): # to get specific files
    #         videos.append(file)
    #     if file.endswith(".avi"): # to get specific files
    #         videos.append(file)
    #     if file.endswith(".wav"): # to get specific files
    #         videos.append(file)
    #     if file.endswith(".mov"): # to get specific files
    #         videos.append(file)

    return videos

def list_frames_by_path(path):
    frames = []
    for file in os.listdir(os.path.abspath(path)):
        # if file.endswith(".plf"): # to get specific files
        #     frames.append(file)
        if file.endswith(".jpg"): # to get specific files
            frames.append(file)
        if file.endswith(".png"): # to get specific files
            frames.append(file)
        if file.endswith(".bmp"): # to get specific files
            frames.append(file)
    return frames

def list_gt_frames_by_path(path):
    frames = []
    for file in os.listdir(os.path.abspath(path)):
        if file.endswith(".plf"): # to get specific files
            frames.append(file)
        # if file.endswith(".jpg"): # to get specific files
        #     frames.append(file)
        # if file.endswith(".png"): # to get specific files
        #     frames.append(file)
        # if file.endswith(".bmp"): # to get specific files
        #     frames.append(file)
    return frames
