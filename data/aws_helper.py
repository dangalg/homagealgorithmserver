import os

__author__ = 'dangalg'

# Import the SDK
import boto
from boto.s3.key import Key

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

s3 = boto.connect_s3()

# conn = boto.connect_s3(
#         aws_access_key_id = access_key,
#         aws_secret_access_key = secret_key,
#         host = 'objects.dreamhost.com',
#         #is_secure=False,               # uncomment if you are not using ssl
#         calling_format = boto.s3.connection.OrdinaryCallingFormat(),
#         )

def uploadfiletos3(bucketname, keyname, localfilename):
    homagealgobucket = s3.get_bucket(bucketname)
    k = Key(homagealgobucket)
    k.key = keyname
    k.set_contents_from_filename(localfilename)


def downloadfilefroms3(bucketname, keyname, localfilename):
    homagealgobucket = s3.get_bucket(bucketname)
    k = Key(homagealgobucket)
    k.key = keyname
    k.get_contents_to_filename(localfilename)


def downloadfolderfroms3(bucketname, keyname, localfoldername):
    homagealgobucket = s3.get_bucket(bucketname)
    boto.logging.info('Downloading video ' + keyname)
    for key in homagealgobucket.get_all_keys(prefix=keyname):
        try:
            head, tail = os.path.split(localfoldername + '/' + key.name)
            if not os.path.exists(head):
                os.makedirs(head)
            res = key.get_contents_to_filename(localfoldername + '/' + key.name)
        except IOError as e:
            boto.logging.info(str(e.args).replace("'", ""))
    boto.logging.info('Finished Downloading video ' + keyname)


def listfolderfroms3(bucketname, keyname):
    homagealgobucket = s3.get_bucket(bucketname)
    boto.logging.info('Listing videos for: ' + keyname)
    videos = []
    for key in homagealgobucket.get_all_keys(prefix=keyname, delimiter='/'):
        try:
            # twice because first it removes / then splits
            directory, videoname = os.path.split(key.name)
            directory, videoname = os.path.split(directory)
            videos.append(videoname)
        except IOError as e:
            boto.logging.info(str(e.args).replace("'", ""))
    boto.logging.info('Finished Listing videos')
    # Remove keyname from list
    videos.remove(os.path.split(keyname)[0])
    for v in videos:
        boto.logging.info(v)
    return videos