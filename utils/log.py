__author__ = 'danga_000'

from file import fileIO

#log errors to file
def log_errors(error):
    f = fileIO.get_file_by_name_write("C:\\testhomage\\log.txt")
    f.write(error)