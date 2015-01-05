import os
import pymysql

__author__ = 'danga_000'

connection=None
def get_connection():

    # env = os.getenv('SERVER_SOFTWARE')
    # if (env and env.startswith('Google App Engine/')):
    #     # Connecting from App Engine
    #     db = MySQLdb.connect(
    #     unix_socket='/cloudsql/homage-automation:homage-instance-db',
    #     user='root')
    # else:
    #       # Connecting from an external network.
    #     # Make sure your network is whitelisted
    #     db = MySQLdb.connect(
    #     host='173.194.86.16',
    #     port=3306,
    #     user='root')

        # cursor = db.cursor()
        # cursor.execute('SELECT 1 + 1')
    global connection
    if not connection:
        connection = pymysql.connect(host="173.194.86.16", # your host, usually localhost
                                     port=3306,
                                     user="root", # your username
                                     passwd="Homageit10", # your password
                                     db="homage") # name of the data base
        connection.autocommit(True)
    return connection

def get_cursor_from_query(query):
    # you must create a Cursor object. It will let
    #  you execute all the query you need
    connection = get_connection()
    cur = connection.cursor()
    # Use all the SQL you like
    cur.execute(query)
    return cur

def dml(query):
    cursor = get_cursor_from_query(query)

