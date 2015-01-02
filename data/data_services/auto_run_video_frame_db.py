from models.autorunvideoframe import AutoRunVideoFrame

__author__ = 'danga_000'
from data import db


# def get_AutoRunVideoFrame_by_cycleidvideoidframeid(cycleid,videoid,frameid):
#     query = "SELECT * FROM AutoRunVideoFrame " \
#             "WHERE cycle_id = {0} AND video_id = {1} AND frame_id = {2}".format(cycleid,videoid,frameid)
#     cursor = db.get_cursor_from_query(query)
#     row = cursor.fetchone()
#     if row:
#         autorunvideoframe = AutoRunVideoFrame(row[0],row[1],row[2],row[3])
#         return autorunvideoframe


def insert_autorunvideoframe(autorunvideoframe):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO AutoRunVideoFrame(cycle_id,
         video_id, frame_id, score, frame_exception)
         VALUES ({0}, {1}, {2}, {3},'{4}')""".format(autorunvideoframe.cycleid,
                                                 autorunvideoframe.videoid,
                                                 autorunvideoframe.frameid,
                                                 autorunvideoframe.score,
                                                 autorunvideoframe.frameexception)
    db.dml(query)

# def update_score(autorunvideoframe,score):
#     # Prepare SQL query to UPDATE required records
#     query = "UPDATE AutoRunVideoFrame SET score = {0}  WHERE cycle_id = {1} AND video_id = {2} AND frame_id = {3}".format(score,
#                                                                                    autorunvideoframe.cycleid,
#                                                                                    autorunvideoframe.videoid,
#                                                                                    autorunvideoframe.frameid)
#     db.dml(query)
#
def delete_autorunvideoframes_by_cycleidvideoid(cycleid, videoid):
    # Prepare SQL query to UPDATE required records
    query = "DELETE FROM AutoRunVideoFrame WHERE cycle_id = {0} AND video_id = {1}".format(cycleid,videoid)
    db.dml(query)