import pymysql

__author__ = 'danga_000'

connection=None
def get_connection():
    global connection
    if not connection:
        connection = pymysql.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="1234", # your password
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

