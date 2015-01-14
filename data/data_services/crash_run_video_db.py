__author__ = 'dangalg'

from models.crash_run_video import CrashRunVideo


from data import db

def get_top_crashrunvideo_id():
    query = "SELECT * FROM crashrunvideo ORDER BY crashrunvideo_id DESC LIMIT 1"
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        crashrunvideo = CrashRunVideo(row[0],row[1],row[2],row[3])
        return crashrunvideo.crashrunvideoid

def get_crashrunvideo_by_cycleidvideoid(cycleid,videoid):
    query = "SELECT * FROM crashrunvideo " \
            "WHERE cycle_id = {0} AND video_id = {1}".format(cycleid,videoid)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        autorunvideo = CrashRunVideo(row[0],row[1],row[2],row[3])
        return autorunvideo


def insert_crash_run_video(crashrunvideo):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO crashrunvideo(crashrunvideo_id, cycle_id, video_id, crvexception)
         VALUES ({0}, {1}, {2}, '{3}')""".format(crashrunvideo.crashrunvideoid, crashrunvideo.cycleid,
                                                 crashrunvideo.videoid,
                                                 crashrunvideo.crvexception)
    db.dml(query)


def update_crashrunvideo(crashrunvideo):
    # Prepare SQL query to UPDATE required records
    query = "UPDATE crashrunvideo SET crvexception = '{0}' " \
            "WHERE cycle_id = {1} AND video_id = {2}".format(crashrunvideo.crvexception,
                                                             crashrunvideo.cycleid,
                                                             crashrunvideo.videoid)
    db.dml(query)