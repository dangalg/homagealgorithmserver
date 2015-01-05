from data import db
from models.video import Video

__author__ = 'danga_000'

def get_top_video_id():
    query = "SELECT * FROM videos ORDER BY video_id DESC LIMIT 1"
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        video = Video(row[0],row[1],row[2],row[3],row[4])
        return video.videoid

def get_all_videos():
    vids = []
    query = "SELECT * FROM videos"
    cursor = db.get_cursor_from_query(query)
    videos = cursor.fetchall()
    for row in videos:
        vid = Video(row[0],row[1],row[2],row[3],row[4])
        vids.append(vid)
    return vids

def get_videos_by_search(query):
    vids = []
    query = "SELECT * FROM videos WHERE video_name LIKE '%{0}%'".format(query)
    cursor = db.get_cursor_from_query(query)
    videos = cursor.fetchall()
    for row in videos:
        vid = Video(row[0],row[1],row[2],row[3],row[4])
        vids.append(vid)
    return vids

def get_video_by_id(id):
    query = "SELECT * FROM videos WHERE video_id = '{0}'".format(id)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        vid = Video(row[0],row[1],row[2],row[3],row[4])
        return vid

def get_video_by_name(name):
    query = "SELECT * FROM videos WHERE video_name = '{0}'".format(name)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        vid = Video(row[0],row[1],row[2],row[3],row[4])
        return vid

def insert_video(video):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO videos(video_id,
         video_name, num_of_frames, video_path, ffmpeg)
         VALUES ({0}, '{1}', {2}, '{3}', {4})""".format(video.videoid,video.videoname,video.numofframes,video.path,video.ffmpeg)
    db.dml(query)

def update_video_by_id(id,video):
    # Prepare SQL query to UPDATE required records
    query = "UPDATE videos SET video_name = '{0}', num_of_frames = {1},video_path = '{2}',ffmpeg = {3}  " \
            "WHERE video_id = {4}".format(video.videoname,video.numofframes,video.path,video.ffmpeg,id)
    db.dml(query)

def delete_video_by_id(id):
    # Prepare SQL query to UPDATE required records
    query = "DELETE FROM videos WHERE video_id = {0}".format(id)
    db.dml(query)