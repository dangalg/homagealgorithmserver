# import setuppyffmpeg
import os
from runcycle.cycle import run_cycle

__author__ = 'danga_000'

# setuppyffmpeg.setup()


from logic.logic_services import general_param_logic

gps = general_param_logic.get_general_params()
# # print gps['AlgorithmOutput']
#print gps


run_cycle()

# os.path.abspath('mydir/myfile.txt')
# print os.path.abspath(gps['AlgorithmOutput'] + "/" + gps['AlgorithmVersion'])


