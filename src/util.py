import json
import re
import os
import shutil

import config
from const import *

def extract_youtube_id(s):
    s = re.sub(' //.*$', '', s)
    a = s.split("v=")
    if len(a) == 1:
        return s
    return a[1].split("&")[0]

def dump_data():
    groups = parse()
    for group in groups:
        print(group[TITLE])
        print(','.join(group[LIST]))
        print()

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def read_api_data(f):
    data = json.load(open(f))
    result = {}
    for item in data["items"]:
        result[id] = read_single_video_obj(item)
    return result

def read_single_video_json(f):
    return read_single_video_obj(json.load(open(f)))

def read_single_video_obj(item):
    id = item["id"]
    snippet = item["snippet"]
    title = snippet["title"]
    thumbnail_url = snippet["thumbnails"]["high"]["url"]
    channel_id = snippet["channelId"]
    channel_title = snippet["channelTitle"]
   
    return {
      ID: id,
      TITLE: title,
      THUMBNAIL_URL: thumbnail_url,
      CHANNEL_ID: channel_id,
      CHANNEL_TITLE: channel_title,
    }
    

def get_cache_files():
    return os.listdir(config.CACHE_DIR)

def get_cache_path(id):
    return "%s/%s" % (config.CACHE_DIR, id)

# copy all files inside src to dst, non recursive
def copy_all(src, dst):
    for f in os.listdir(src):
        shutil.copy("%s/%s" % (src, f), "%s/%s" % (dst, f))


if __name__ == "__main__":
    tests = [
        "IDI6xi9z3Zk",
        "/watch?v=IDI6xi9z3Zk",
        "/watch?v=IDI6xi9z3Zk //comment",
        "/watch?v=IDI6xi9z3Zk&t=1",
        "/watch?v=IDI6xi9z3Zk&t=1 //comment",
    ]
    for t in tests:
        print(extract_youtube_id(t))
