import subprocess

__author__ = 'danga_000'


def ffmpeg_on_path(filename):
    # ffmpeg on computer
    framename = filename.split('.')[0]
    ffmpeg_command = "ffmpeg -i {0} -q:v 1 {1}-%4d.jpg".format(filename,framename)
    p = subprocess.Popen(ffmpeg_command, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
