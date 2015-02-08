from utils import consts

__author__ = 'dangalg'
import json


def read_json_file():
    json_data=open(consts.progressjson)
    data = json.load(json_data)
    json_data.close()
    return data

def write_to_json(data):
    with open(consts.progressjson, 'w') as outfile:
        json.dump(data, outfile)

def update_progress_json(status, progress, max, algo_version):
     data ={"algorun":{"status":status, "value":progress, "max":max, "algo_version":algo_version}}
     write_to_json(data)

def get_progress_json():
    read_json_file()
