import json
import re
import os
import shutil

import config
from lib.const import *

def extract_youtube_id(s):
    s = re.sub(' //.*$', '', s)
    a = s.split("v=")
    if len(a) == 1:
        return s
    return a[1].split("&")[0]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_cache_files():
    return os.listdir(config.CACHE_DIR)

def get_cache_path(id):
    return "%s/%s" % (config.CACHE_DIR, id)

# copy all files inside src to dst, non recursive
def copy_all(src, dst):
    for f in os.listdir(src):
        shutil.copy("%s/%s" % (src, f), "%s/%s" % (dst, f))

def sort_videos(video_data):
    ids = video_data.keys()
    most_viewed = sorted(ids, key=lambda id: -int(video_data[id][VIEW_COUNT]))
    latest = sorted(ids, key=lambda id: video_data[id][PUBLISHED_AT], reverse=True)

    return (most_viewed, latest)

def dump_video_list(ids, video_data):
    return ["%s // %s" % (id, video_data[id][TITLE]) for id in ids]

