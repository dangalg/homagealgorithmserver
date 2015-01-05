from models.autorunvideo import AutoRunVideo

__author__ = 'danga_000'


from data import db

def get_AutoRunVideo_by_cycleidvideoid(cycleid,videoid):
    query = "SELECT * FROM autorunvideo " \
            "WHERE cycle_id = {0} AND video_id = {1}".format(cycleid,videoid)
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        autorunvideo = AutoRunVideo(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
        return autorunvideo

def insert_autorunvideo(autorunvideo):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO autorunvideo(cycle_id,
         video_id, average_score, avexception, variance_score, final_score, aws_output)
         VALUES ({0}, {1}, {2}, '{3}', {4}, {5},'{6}')""".format(autorunvideo.cycleid,
                                                 autorunvideo.videoid,
                                                 autorunvideo.averagescore,
                                                 autorunvideo.avexception,
                                                 autorunvideo.variancescore,
                                                 autorunvideo.finalscore,
                                                 autorunvideo.awsoutput)
    db.dml(query)

def update_autorunvideo(autorunvideo):
    # Prepare SQL query to UPDATE required records
    query = "UPDATE autorunvideo SET average_score = {0}, avexception = '{1}', variance_score = {2}, final_score = {3}, aws_output = '{4}' " \
            "WHERE cycle_id = {5} AND video_id = {6}".format(autorunvideo.averagescore,
                                                             autorunvideo.avexception,
                                                             autorunvideo.variancescore,
                                                             autorunvideo.finalscore,
                                                             autorunvideo.awsoutput,
                                                             autorunvideo.cycleid,
                                                             autorunvideo.videoid)
    db.dml(query)
#
def delete_autorunvideo_by_cycleidvideoid(autorunvideo):
    # Prepare SQL query to UPDATE required records
    query = "DELETE FROM autorunvideo WHERE cycle_id = {0} AND video_id = {1}".format(autorunvideo.cycleid,autorunvideo.videoid,)
    db.dml(query)