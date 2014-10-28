from logic.logic_services import general_param_logic

__author__ = 'danga_000'

from file import fileIO

#log errors to file
def log_errors(error):
    gps = general_param_logic.get_general_params()
    f = fileIO.get_file_by_name_write(gps['VideoFolder'] + '/log.txt')
    f.write(error)