import json
import re
import os
import shutil
import isodate

import config
from const import *

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
    content_details = item["contentDetails"]
    stat = item["statistics"]

    title = snippet["title"]
    thumbnail_url = snippet["thumbnails"]["high"]["url"]
    channel_id = snippet["channelId"]
    channel_title = snippet["channelTitle"]
    raw_published_at = snippet["publishedAt"]
    raw_duration = content_details["duration"]
    view_count = stat["viewCount"]

    published_at = formate_date(raw_published_at)
    duration = format_duration(raw_duration)
   
    return {
      ID: id,
      TITLE: title,
      THUMBNAIL_URL: thumbnail_url,
      CHANNEL_ID: channel_id,
      CHANNEL_TITLE: channel_title,
      DURATION: duration,
      VIEW_COUNT: view_count,
      PUBLISHED_AT: published_at,
    }

def format_duration(raw_duration):
    total = isodate.parse_duration(raw_duration).total_seconds()
    hour = total / 3600
    minute = (total / 60) % 60
    sec = total % 60

    if minute < 60:
        return "%d:%02d" % (minute, sec)
    return "%d:%02d:%02d" % (hour, minute, sec)

def formate_date(raw_date):
    return isodate.parse_date(raw_date)

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
