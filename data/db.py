
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

def insert(self, query):
    try:
        self.cursor.execute(query)
        self.connection.commit()
    except:

        self.connection.rollback()

# class Database:
#
#     host = 'localhost'
#     user = 'root'
#     password = ''
#     db = 'homage'
#
#     def __init__(self):
#         self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
#         self.cursor = self.connection.cursor()
#
#     def insert(self, query):
#         try:
#             self.cursor.execute(query)
#             self.connection.commit()
#         except:
#             self.connection.rollback()
#
#     def query(self, query):
#         cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
#         cursor.execute(query)
#
#         return cursor.fetchall()
#
#     def __del__(self):
#         self.connection.close()

