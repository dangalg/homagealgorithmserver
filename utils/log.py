from logic.logic_services import general_param_logic
from utils import consts

__author__ = 'danga_000'

from file import fileIO

#log errors to file
def log_information(gps, error):
    if gps[consts.crashrunname].val:
        fileIO.get_file_by_name_write(gps[consts.crashrunvideofoldername].val + 'log.txt').write(error)
    else:
        fileIO.get_file_by_name_write(gps[consts.videofoldername].val + 'log.txt').write(error)
