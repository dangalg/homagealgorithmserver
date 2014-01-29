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

def get_objects_from_query(query):

    # you must create a Cursor object. It will let
    #  you execute all the query you need
    if connection:
        cur = connection.cursor()
        # Use all the SQL you like
        cur.execute(query)
        # print all the first cell of all the rows
        for row in cur.fetchall() :
            print row[0]
    else:
        print "Must connect to db first. use db.get_connection().cursor()"