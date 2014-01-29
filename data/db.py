
import MySQLdb

__author__ = 'danga_000'

connection=None
def get_connection():
    global connection
    if not connection:
        connection = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="", # your password
                      db="homage") # name of the data base
    return connection

def get_cursor_from_query(query):
    # you must create a Cursor object. It will let
    #  you execute all the query you need
    get_connection()
    cur = connection.cursor()
    # Use all the SQL you like
    cur.execute(query)
    return cur

def dml(self, query):
    cursor = get_cursor_from_query(query)
    try:
        # Commit your changes in the database
        cursor.commit()
    except:
        # Rollback in case there is any error
        cursor.rollback()
        # TODO log error

