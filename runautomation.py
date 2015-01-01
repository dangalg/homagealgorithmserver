from runcycle.cycle import run_cycle

__author__ = 'dangalg'

import sys

optimize = 0
algoversion = None
mainfolder = None

# Get Parameters
if len(sys.argv) < 3:
    print('Not enough arguments')
    print("Input needed: optimise?(default = 0) algorithm_version main_folder (also you should have a params.xml file in the main folder)")
elif len(sys.argv) > 4:
    print('Too many cooks! um.. arguments..')
    print("Input needed: optimise?(1 or 0 default = 0) algorithm_version main_folder (also you should have a params.xml file in the main folder)")
elif len(sys.argv) == 3:
    algoversion = sys.argv[1]
    mainfolder = sys.argv[2]
elif len(sys.argv) == 4:
    optimize = sys.argv[1]
    algoversion = sys.argv[2]
    mainfolder = sys.argv[3]
else:
    print("Woah cowboy")

run_cycle(str(optimize), str(algoversion), str(mainfolder))
