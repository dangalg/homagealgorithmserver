from runcycle.run_cycle import run_cycle

__author__ = 'dangalg'

import sys

optimize = 0
algoversion = None
mainfolder = None
crashrun = 0
updatedb = 0
message = "Input needed:\nupdatedb?(1 or 0 should I replace data or just add the new data) " \
          "\ncrashrun?(1 or 0 test the movies in the CrashRunVideos folder) \noptimise?(1 or 0)  \nalgorithm_version \nmain_folder \n(also you should have a params.xml file in the main folder)"

# Get Parameters
if len(sys.argv) < 6:
    print('Not enough arguments')
    print(message)
elif len(sys.argv) > 6:
    print('Too many cooks! um.. arguments..')
    print(message)
elif len(sys.argv) == 6:
    crashrun = sys.argv[1]
    optimize = sys.argv[2]
    updatedb = sys.argv[3]
    algoversion = sys.argv[4]
    mainfolder = sys.argv[5]
    run_cycle(str(crashrun), str(optimize), str(updatedb), str(algoversion), str(mainfolder))
else:
    print("Woah cowboy")


