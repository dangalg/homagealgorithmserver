__author__ = 'danga_000'
from models import general_param
from data import db

curs = db.get_connection().cursor()

curs.close()


