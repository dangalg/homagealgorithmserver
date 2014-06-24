from data.data_services import algorithm_version_db

__author__ = 'danga_000'


def get_last_algorithm_version():
    return algorithm_version_db.get_last_algorithm_version()

def get_all_algo_versions():
    return algorithm_version_db.get_all_algo_versions()

def insert_algo_version(version):
    algorithm_version_db.insert_algo_version(version)