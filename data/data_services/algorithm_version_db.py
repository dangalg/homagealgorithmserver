from models.algorithmversion import AlgorithmVersion

__author__ = 'danga_000'

from data import db

def get_last_algorithm_version():
    query = "SELECT * FROM algorithmversions ORDER BY algo_version DESC LIMIT 1"
    cursor = db.get_cursor_from_query(query)
    row = cursor.fetchone()
    if row:
        algoversion = AlgorithmVersion(row[0])
        return algoversion.algoversion

def get_all_algo_versions():
    versions = []
    query = "SELECT * FROM algorithmversions"
    cursor = db.get_cursor_from_query(query)
    algo_versions = cursor.fetchall()
    for row in algo_versions:
        algo_version = AlgorithmVersion(row[0])
        versions.append(algo_version)
    return versions

def insert_algo_version(version):
    # Prepare SQL query to INSERT a record into the database.
    query = """INSERT INTO algorithmversions(algo_version)
         VALUES ('{0}')""".format(version)
    db.dml(query)
